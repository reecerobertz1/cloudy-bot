import discord
from setup.config import contribs_simple, contribs
from setup.config import community_id
from typing import Union, Optional
from utils.subclasses import CloudyBot
from discord.interactions import Interaction
import html
import random
from string import ascii_uppercase
import asyncio

class QuestionFetchFailed(Exception):
    pass

class ShowGiveawayContributers(discord.ui.View):
    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

    @discord.ui.button(label="Show guide", style=discord.ButtonStyle.blurple)
    async def guide_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != discord.Member:
            chroma_community = interaction.client.get_guild(community_id)
            if chroma_community == None:
                chroma_community = await interaction.client.fetch_guild(community_id)
            member = chroma_community.get_member(interaction.user.id)
            if member == None:
                member = await chroma_community.fetch_member(interaction.user.id)
        else:
            member = interaction.user
        if member is None:
            return await interaction.response.send("You need to be in the Chroma Community server to use this button")
        if member.is_on_mobile() == True:
            await interaction.response.send_message(contribs_simple, ephemeral=True)
        else:
            await interaction.response.send_message(contribs, ephemeral=True)

class QuizStarter(discord.ui.View):
    def __init__(self, participants: list, embed: discord.Embed, moderator: Union[discord.Member, discord.User], difficulty: str, category: int, question_count: int, category_name: str, message: discord.Message, bot: CloudyBot):
        self.participants = participants
        self.embed = embed
        self.moderator = moderator
        self.scores = {}
        self.questions = []
        self.current_question = 0
        self.scorers = []
        self.correct_answer = ""
        self.have_submitted = []
        self.bot = bot
        self.difficulty = difficulty
        self.category = category
        self.question_count = question_count
        self.category_name = category_name
        self.answer = ""
        self.message = message

        super().__init__(timeout=90)

    async def get_questions(self) -> None:
        """Gets questions from open trivia database"""
        async with self.bot.session.get(f"https://opentdb.com/api.php?amount={self.question_count}&category={self.category}&difficulty={self.difficulty}&type=multiple") as response:
            json = await response.json()
            if json["response_code"] != 0:
                raise QuestionFetchFailed("Couldn't get questions")
            else:
                for question in json["results"]:
                    self.questions.append(question)

    def get_question(self) -> tuple[str, list, str]:
        """Gets question and answers from questions list"""
        question_info = self.questions[0]
        question = question_info["question"]
        answers = [question_info["correct_answer"]]
        for i_q in question_info["incorrect_answers"]:
            answers.append(i_q)
        random.shuffle(answers)
        keyed_answers = []
        correct_answer = ""
        for i, q in zip(ascii_uppercase, answers):
            keyed_answers.append({i: q})
            if q == question_info["correct_answer"]:
                correct_answer = i
        self.questions.pop(0)
        self.current_question += 1
        self.answer = question_info["correct_answer"]
        return question, keyed_answers, correct_answer
    
    def get_scoreboard(self) -> str:
        """Creats the scoreboard to send when quiz ends"""
        sorted_scores = sorted(self.scores.items(), key=lambda x: x[1], reverse=True)
        board_text = ""

        for i, (user_id, score) in enumerate(sorted_scores):
            place = i + 1
            suffix = "st" if place == 1 else "nd" if place == 2 else "rd" if place == 3 else "th"
            board_text += f"\n\n**{place}{suffix} place**\n<@!{user_id}> [{score}]"

        return board_text

    async def start_quiz(self, interaction: Interaction) -> None:
        """Main quiz function"""
        self.clear_items()
        for userid in self.participants:
            self.scores[userid] = 0
        try:
            await self.get_questions()
        except QuestionFetchFailed:
            embed = discord.Embed(title="Error!", description=f"I couldn't find questions under the following parameters *{self.category_name} - {self.question_count} questions - {self.difficulty}*")
            return await interaction.message.edit(embed=embed)
        while len(self.questions) > 0:
            question, answers, correct_answer = self.get_question()
            formatted_question = html.unescape(question)
            embed = discord.Embed(title="Quiz", description=f"Question {self.current_question}\n**{formatted_question}**", color=0x3e5bab)
            embed.set_footer(text=f"{self.difficulty.capitalize()} | {self.category_name.capitalize()} | {self.question_count} questions")
            for answer_dict in answers:
                for key, value in answer_dict.items():
                    formatted_answer = html.unescape(value)
                    embed.add_field(name=key, value=formatted_answer, inline=False)
            self.embed = embed
            self.correct_answer = correct_answer
            self.add_item(QuizButton("A", self))
            self.add_item(QuizButton("B", self))
            self.add_item(QuizButton("C", self))
            self.add_item(QuizButton("D", self))
            try:
                await interaction.message.edit(view=self, embed=embed)
            except:
                await interaction.message.edit(view=self, embed=embed)
            while self.have_submitted < self.participants:
                await asyncio.sleep(4)
            self.clear_items()
            if len(self.scorers) > 0:
                embed = discord.Embed(title="Quiz", description=f"The correct answer was `{correct_answer}: {self.answer}`\n\n{', '.join(self.scorers[:-1]) + f' and {self.scorers[-1]}' if len(self.scorers) > 1 else self.scorers[0]} got it right!", color=0x3e5bab)
            else:
                embed = discord.Embed(title="Quiz", description=f"The correct answer was `{correct_answer}: {self.answer}`\n\nNobody answered correctly.", color=0x3e5bab)
            await interaction.message.edit(embed=embed)
            await asyncio.sleep(5)
            self.scorers.clear()
            self.have_submitted.clear()
        scoreboard = self.get_scoreboard()
        embed = discord.Embed(title="Results", description=scoreboard, color=0x3e5bab)
        await interaction.message.edit(embed=embed, view=None)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple)
    async def join(self, interaction: Interaction, _):
        await interaction.response.defer()
        if interaction.user.id not in self.participants:
            self.participants.append(interaction.user.id)
        else:
            return await interaction.followup.send("You already joined!", ephemeral=True)
        i = len(self.embed.fields) + 1
        embed = self.embed.add_field(name=f"{i}", value=f"**{interaction.user.display_name}**", inline=False)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(label="Start quiz", style=discord.ButtonStyle.green)
    async def quiz_starter(self, interaction: Interaction, _):
        await interaction.response.defer()
        if interaction.user.id != self.participants[0]:
            return await interaction.followup.send(f"Only {self.moderator.display_name} can start the quiz!", ephemeral=True)
        await self.start_quiz(interaction)

class QuizButton(discord.ui.Button):
    def __init__(self, label: str, quiz_class: QuizStarter) -> None:
        super().__init__(label=label, style=discord.ButtonStyle.blurple)
        self.answer = label
        self.quiz = quiz_class
        self.scorers = []

    async def interaction_check(self, interaction: Interaction) -> bool:
        return interaction.user.id in self.quiz.participants

    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.defer()
        if interaction.user.id in self.quiz.have_submitted:
            return
        if self.quiz.correct_answer == self.answer:
            self.quiz.scores[interaction.user.id] = self.quiz.scores[interaction.user.id] + 1
            self.quiz.scorers.append(interaction.user.display_name)
        self.quiz.have_submitted.append(interaction.user.id)