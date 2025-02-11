from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

hashtags = ["#Volunteering",
"#YouthProjects",
"#Education",
"#Career",
"#Internships",
"#Networking",
"#Scholarships",
"#ErasmusPlus",
"#Leadership",
"#Events",
"#PersonalDevelopment",
"#Community",
"#StudentLife",
"#NGO",
"#Workshops",
"#SoftSkills",
"#Teamwork",
"#Innovation",
"#Sustainability",
"#CulturalExchange",
"#Eco",
"#ArtAndCulture",
"#Language",
"#ClimateAction",
"#Europ"
]


def inlinetags1():
	keyboard = InlineKeyboardBuilder()
	for elem in hashtags:
		keyboard.add(InlineKeyboardButton(text=elem, callback_data=elem))
	return keyboard.adjust(2).as_markup()

