from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

timelist = ["8:00", "13:00", "21:00", "Realtime"]

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


def settime():
	keyboard = InlineKeyboardBuilder()
	for elem in timelist:
		keyboard.add(InlineKeyboardButton(text=elem, callback_data=elem))
	return keyboard.adjust(1).as_markup()


def inlinetags1():
	keyboard = InlineKeyboardBuilder()
	for elem in hashtags:
		keyboard.add(InlineKeyboardButton(text=elem, callback_data=elem))
	return keyboard.adjust(2).as_markup()

