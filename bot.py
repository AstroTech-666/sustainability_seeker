from datetime import timedelta
from telegram import CallbackQuery, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, CallbackQueryHandler
import logging
import random
import os
from flask import Flask
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.INFO)

# List of sections and their corresponding links
SECTIONS_WITH_LINKS = {
"Renewable Energy": [
    "https://gwcnweb.org/members/membership-application",
    "https://www.seai.ie/plan-your-energy-journey/for-your-community/sustainable-energy-communities/start-an-energy-community",
    "https://www.renewableenergyworld.com",
    "https://ases.org",
    "https://acespace.org",
    "https://www.irena.org",
    "https://www.aeecenter.org",
    "https://www.reddit.com/r/RenewableEnergy",
    "https://www.solarpowerworldonline.com",
    "https://www.linkedin.com/groups/2121068",
    "https://www.linkedin.com/groups/4280062"
    ],
   "Waste Management": [
   "https://waste-management-world.com",
   "https://www.reddit.com/r/wastemanagement",
   "https://www.facebook.com/groups/composting101",
   "https://www.linkedin.com/groups/2022870",
   "https://onetreeplanted.org/pages/individuals",
   "http://www.globalrecyclingnetwork.com",
   "https://www.iswa.org",
   "https://www.wastedive.com",
   "https://kab.org",
   "https://recyclingpartnership.org"
    ],
 "Water Conservation": [
    "https://www.awwa.org",
    "https://www.reddit.com/r/waterconservation",
    "https://www.allianceforwaterefficiency.org",
    "https://water.org",
    "https://iwa-network.org",
    "https://cleanwater.org",
    "https://www.linkedin.com/groups/888527",
    "https://www.instagram.com/generosity_org",
    "https://lifewater.org",
    "https://www.instagram.com/water_conservation_project"
    ],
"Sustainable Agriculture": [
    "https://rodaleinstitute.org",
    "https://sustainableagriculture.net",
    "https://www.reddit.com/r/Agriculture",
    "https://www.sare.org",
    "https://agfunder.com",
    "https://sustainablefoodtrust.org",
    "https://www.organic-center.org",
    "https://farmersmarketcoalition.org",
    "https://www.linkedin.com/groups/4673163",
    "https://www.linkedin.com/groups/1691777"
    ],
"Climate Policy": [
    "https://climatenetwork.org",
    "https://www.climaterealityproject.org",
    "https://www.reddit.com/r/climate",
    "https://www.c2es.org",
    "https://www.edf.org",
    "https://www.redeycl.org",
    "https://www.linkedin.com/groups/1140337",
    "https://www.linkedin.com/groups/13622996",
    "https://350.org",
    "https://www.theclimategroup.org"
    ],
"Community Engagement": [
    "https://fridaysforfuture.org",
    "https://www.sdsnyouth.org",
    "https://www.earthguardians.org",
    "https://www.unicef.org/innovation/take-action",
    "https://www.genevaenvironmentnetwork.org/resources/updates/youth-and-the-environment",
    "https://education-for-climate.ec.europa.eu/community/Callforyoungmembers",
    "https://worlded.org/work-for-us",
    "https://www.instagram.com/youth_for_development_and_sg",
    "https://www.instagram.com/yfs.in",
    "https://www.linkedin.com/groups/9033600"
    ],
"Biodiversity": [
    "https://www.birdlife.org",
    "https://iucn.org",
    "https://www.wri.org",
    "https://www.worldwildlife.org",
    "https://www.conservation.org",
    "https://www.biodiversitylibrary.org",
    "https://earthwatch.org",
    "https://www.projectnoah.org",
    "https://www.nationalgeographic.org/society",
    "https://www.gbif.org",
    "https://www.linkedin.com/groups/2620686"
    ],
"Carbon Footprint Reduction": [
    "https://www.carbontrust.com/en-as",
    "https://www.carbonfootprint.com/careers.html",
    "https://www.changeclimate.org",
    "https://carbonfootprintchallenge.org",
    "https://drawdown.org",
    "https://www.earthday.org",
    "https://www.greenpeace.org/international",
    "https://www.instagram.com/carbonfootprintfoundation",
    "https://www.reddit.com/r/CarbonFootprint",
    "https://www.linkedin.com/groups/107977"
    ],
"Climate Justice": [
    "https://climatejusticealliance.org",
    "https://movementgeneration.org",
    "https://ejfoundation.org",
    "https://www.climaterealityproject.org",
    "https://www.weact.org/home-3-2-2-2/getinvolved/membership/cjwg",
    "https://www.linkedin.com/groups/9396139",
    "https://www.linkedin.com/groups/14357555",
    "https://www.reddit.com/r/climatejustice",
    "https://www.instagram.com/climate.justice_/",
    "https://www.cbecal.org/issues/climate-justice"
    ],
"Sustainable Transportation": [
    "https://transalt.org",
    "https://activetrans.org",
    "https://bikeleague.org",
    "https://iclei.org",
    "https://smartergrowth.net",
    "https://www.walkscore.com",
    "https://www.linkedin.com/groups/1103027",
    "https://www.linkedin.com/groups/3201081",
    "https://www.reddit.com/r/electricvehicles",
    "https://www.transportationandclimate.org/content/sustainable-communities"
    ],
"Recycling and Circular Economy": [
    "https://www.ellenmacarthurfoundation.org",
    "https://recyclingpartnership.org",
    "https://www.circulareconomyclub.com",
    "https://earth911.com",
    "https://greenblue.org",
    "https://www.plasticpollutioncoalition.org",
    "https://www.reddit.com/r/circular_economy",
    "https://www.linkedin.com/groups/14126274",
    "https://www.linkedin.com/groups/10334500",
    "https://www.linkedin.com/groups/82521",
    "https://www.instagram.com/greenhillrecycling"
    ],
"Green Building Practices": [
    "https://living-future.org",
    "https://www.usgbc.org",
    "https://worldgbc.org",
    "https://www.sierrabusiness.org",
    "https://www.buildinggreen.com",
    "https://greenroofs.org",
    "https://www.linkedin.com/groups/4028849",
    "https://www.linkedin.com/groups/2709533",
    "https://www.reddit.com/r/greenbuilding",
    "https://www.instagram.com/green.building"
    ],
"Pollution Control": [
    "https://www.facebook.com/groups/pollutioncontrol",
    "https://www.unsdsn.org",
    "https://www.p2.org",
    "https://www.iaia.org",
    "https://www.reddit.com/r/pollution_masks",
    "https://www.linkedin.com/groups/2106285",
    "https://www.linkedin.com/groups/3785602",
    "https://www.linkedin.com/groups/6713552",
    "https://www.cleanairfund.org/theme/inequality",
    "https://www.epa.gov/ej-research/epa-research-environmental-justice-and-air-pollution"
    ],
"Ecosystem Restoration": [
    "https://www.reddit.com/r/ecologicalrestoration",
    "https://www.ser.org",
    "https://www.nature.org/en-us",
    "https://www.ecosystemrestorationcommunities.org",
    "https://rewildingeurope.com",
    "https://restorationproject.org/wprp",
    "https://www.wildlifetrusts.org",
    "https://www.linkedin.com/groups/5091197",
    "https://www.instagram.com/ecosystem_org",
    "https://www.linkedin.com/groups/6987971"
    ],
"Climate Change Adaptation": [
    "https://www.cakex.org",
    "https://www.nationaladaptationforum.org",
    "https://iclei.org",
    "https://unfccc.int",
    "https://resilientcitiesnetwork.org",
    "https://www.reddit.com/r/ClimateAdaptation",
    "https://www.c40.org",
    "https://www.thegef.org",
    "https://www.adaptationcommunity.net",
    "https://futureearth.org"
    ],
"Sustainable Fisheries": [
    ],
"Environmental Education": [
    ],
"Conservation of Natural Resources": [
    ],
"Smart Cities and Urban Planning": [
    ],
"Environmental Advocacy": [
    ]
}

SECTIONS = list(SECTIONS_WITH_LINKS.keys())

# List of sustainability tips
TIPS = [
    "Reduce plastic use by switching to reusable bags and bottles.",
    "Save energy by turning off lights when not in use.",
    "Choose public transport over driving to reduce your carbon footprint.",
    "Conserve water by fixing leaks and using water-efficient appliances.",
    "Plant trees to help absorb carbon dioxide and provide clean air.",
    "Use energy-efficient light bulbs like LEDs to save electricity.",
    "Compost your food waste to reduce the amount sent to landfills.",
    "Opt for products with minimal packaging to cut down on waste.",
    "Buy locally grown food to reduce transportation emissions.",
    "Install solar panels if possible to harness renewable energy.",
    "Use a programmable thermostat to reduce energy waste when you're not home.",
    "Unplug electronic devices when not in use to prevent 'phantom' energy consumption.",
    "Support brands that prioritize sustainability and ethical practices.",
    "Eat less meat or switch to plant-based meals to lower your carbon footprint.",
    "Avoid single-use plastics like straws, utensils, and containers.",
    "Collect rainwater for gardening and other outdoor uses.",
    "Use natural cleaning products to reduce harmful chemicals in your home.",
    "Recycle electronics at proper facilities to prevent e-waste.",
    "Advocate for climate policies in your community or workplace.",
    "Use bicycles for short distances instead of cars to cut emissions.",
    "Choose energy-efficient appliances when upgrading your home.",
    "Wash clothes in cold water to save energy and extend the life of your garments.",
    "Buy secondhand or upcycled goods to reduce demand for new products.",
    "Turn off your computer or put it in sleep mode when not in use.",
    "Avoid fast fashion by purchasing high-quality, durable clothing."
]

# Dictionary to store subscriptions
subscriptions = {}
feedback_list = []  # List to store feedback

# Flask app to keep the bot alive
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Start Command Handler
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    logging.info(f"User {user_id} started the bot.")
    keyboard = [
        [InlineKeyboardButton("Join Global Online Community", callback_data='global')],
        [InlineKeyboardButton("Subscribe to Updates", callback_data='subscribe')],
        [InlineKeyboardButton("Submit Feedback", callback_data='feedback')],
        [InlineKeyboardButton("Get Daily Tip", callback_data='daily_tip')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to Sustainability Seeker! Choose an option:", reply_markup=reply_markup)

# Feedback Command Handler
async def feedback_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    feedback_text = ' '.join(context.args)  # Get the user's feedback
    if feedback_text:
        feedback_list.append(feedback_text)  # Store feedback in the list
        await update.message.reply_text("Thank you for your feedback!")
    else:
        await update.message.reply_text("Please provide your feedback after the command /feedback.")

async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    logging.info(f"Button clicked: {query.data}")

    handlers = {
        'global': show_sections,
        'subscribe': subscribe,
        'feedback': request_feedback,
        'daily_tip': send_daily_tip,
    }

    if query.data in handlers:
        await handlers[query.data](query)  # Pass only query
    else:
        await show_communities(query, query.data)

    handler = handlers.get(query.data, show_communities)
    await handler(query) if query.data in handlers else await handler(query, query.data)

async def request_feedback(query: CallbackQuery) -> None:
    await query.edit_message_text("Please send your feedback by typing it after the command /feedback.")

async def subscribe(query: CallbackQuery, context: CallbackContext) -> None:
    user_id = query.from_user.id
    if user_id not in subscriptions:
        subscriptions[user_id] = SECTIONS  # Subscribe the user to all sections
        await query.edit_message_text("You have subscribed to updates on all sections.")
        # Schedule daily tips for the user
        context.job_queue.run_daily(send_daily_tip_to_user, time=timedelta(hours=12), context=user_id)  # Send daily tips at noon
    else:
        await query.edit_message_text("You are already subscribed to updates.")

# Send Daily Tip to User
async def send_daily_tip_to_user(context: CallbackContext) -> None:
    user_id = context.job.context
    if user_id in subscriptions:
        tip = random.choice(TIPS)
        await context.bot.send_message(chat_id=user_id, text=f"Here's your daily sustainability tip:\n{tip}")

# Send Daily Tip
async def send_daily_tip(query: CallbackQuery) -> None:
    tip = random.choice(TIPS)
    await query.edit_message_text(f"Here's your daily sustainability tip:\n{tip}")

# Show Sections
async def show_sections(query: CallbackQuery) -> None:
    keyboard = [
        [InlineKeyboardButton(SECTIONS[i], callback_data=SECTIONS[i]),
         InlineKeyboardButton(SECTIONS[i + 1], callback_data=SECTIONS[i + 1])]
        for i in range(0, len(SECTIONS) - 1, 2)
    ]
    
    if len(SECTIONS) % 2 != 0:
        keyboard.append([InlineKeyboardButton(SECTIONS[-1], callback_data=SECTIONS[-1])])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Please choose a section of interest:", reply_markup=reply_markup)

# Show Communities
async def show_communities(query: CallbackQuery, section: str) -> None:
    communities = SECTIONS_WITH_LINKS.get(section, [])
    response_text = f"Communities related to {section}:\n" + "\n".join(f"- {link}" for link in communities)
    
    keyboard = [
        [InlineKeyboardButton(SECTIONS[i], callback_data=SECTIONS[i]),
         InlineKeyboardButton(SECTIONS[i + 1], callback_data=SECTIONS[i + 1])]
        for i in range(0, len(SECTIONS) - 1, 2)
    ]

    if len(SECTIONS) % 2 != 0:
        keyboard.append([InlineKeyboardButton(SECTIONS[-1], callback_data=SECTIONS[-1])])
    
    response_text += "\nChoose another section for more links."
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(response_text, reply_markup=reply_markup)

# Main Function
def main() -> None:
    # Start the Flask app to keep the bot alive
    keep_alive()

    # Initialize the bot
    app = ApplicationBuilder().token('7725726909:AAH2_zrjlGYwx1Pi9Z7tO9LVJWw7VMR6RHQ').build()


    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feedback", feedback_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.run_polling()

if __name__ == '__main__':
    main()
