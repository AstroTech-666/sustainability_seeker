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
    "https://www.irena.org",
    "https://www.nrel.gov",
    "https://www.energy.gov/eere/renewable-energy",
    "https://www.renewableenergyworld.com",
    "https://www.seia.org",
    "https://www.energyinformative.org",
    "https://www.revolutionh2.com",
    "https://www.solarpowerworldonline.com",
    "https://www.electricpowerresearchinstitute.com",
    "https://www.globalwindenergycouncil.org",
    "https://www.energy.gov/solar",
    "https://www.thewindpower.net",
    "https://www.cleantechnica.com",
    "https://www.energystorageassociation.org",
    "https://www.ren21.net",
    "https://www.greenbiz.com",
    "https://www.wisewire.com",
    "https://www.renewablesinternational.net",
    "https://www.ecomena.org",
    "https://www.energymonitor.ai",
    "https://www.solarpowerrocks.com",
    "https://www.cleanenergy.org",
    "https://www.windpowerengineering.com",
    "https://www.energycentral.com",
    "https://www.pvtech.org",
    "https://www.hydroworld.com",
    "https://www.biomassmagazine.com",
    "https://www.nabcep.org",
    "https://www.smartenergydecisions.com",
    "https://www.awea.org",
    "https://www.renewableenergystocks.com",
    "https://www.researchgate.net/publication/324372928_The_future_of_renewable_energy_in_a_circular_economy",
    "https://www.theclimategroup.org"
    ],
   "Waste Management": [
    "https://www.epa.gov/waste",
    "https://www.wm.com",
    "https://www.nrdc.org/issues/waste-management",
    "https://www.nrcan.gc.ca/our-natural-resources/waste-management/10753",
    "https://www.earth911.com",
    "https://www.recycling.com",
    "https://www.solidwasteassociation.org",
    "https://www.waste360.com",
    "https://www.resource-recycling.com",
    "https://www.zerowasteamerica.org",
    "https://www.ciwmb.ca.gov",
    "https://www.recycleacrossamerica.org",
    "https://www.sustainablebusiness.com/waste-management",
    "https://www.rethinkwaste.org",
    "https://www.recyclenow.com",
    "https://www.worldbank.org/en/topic/wastemanagement",
    "https://www.ellenmacarthurfoundation.org/en/our-work/activities/waste-management",
    "https://www.globalwastemanagement.com",
    "https://www.journalofwastemanagement.com",
    "https://www.wastemanagementworld.com",
    "https://www.biocycle.net"
    ],
 "Water Conservation": [
    "https://www.epa.gov/watersense",
    "https://www.water.org",
    "https://www.nrdc.org/issues/water",
    "https://www.worldwildlife.org/initiatives/water",
    "https://www.usgs.gov/mission-areas/water-resources",
    "https://www.wateruseitwisely.com",
    "https://www.waterwatch.org",
    "https://www.americanrivers.org",
    "https://www.watersmart.org",
    "https://www.h2ouse.org",
    "https://www.savewater.com.au",
    "https://www.nationalgeographic.com/environment/article/water-conservation",
    "https://www.groundwater.org",
    "https://www.aqua.org",
    "https://www.savethewater.org",
    "https://www.ceres.org/our-work/water",
    "https://www.waterriskfilter.org",
    "https://www.pacificinstitute.org",
    "https://www.iwra.org",
    "https://www.watercons.org",
    "https://www.unwater.org"
    ],
"Sustainable Agriculture": [
    "https://www.fao.org/sustainable-agriculture",
    "https://www.organic.org",
    "https://www.wwf.org.uk/updates/sustainable-agriculture",
    "https://www.sustainableagriculture.net",
    "https://www.nrdc.org/issues/sustainable-agriculture",
    "https://www.americangrains.com",
    "https://www.globalagriculture.org",
    "https://www.rodaleinstitute.org",
    "https://www.regenerativeagriculture.org",
    "https://www.thefield.ca",
    "https://www.farmers.gov",
    "https://www.sustainableagricultureresearchandeducation.org",
    "https://www.kicktheplastic.org",
    "https://www.earthday.org/campaigns/food-sustainability",
    "https://www.agriculturesnetwork.org",
    "https://www.permaculture.co.uk",
    "https://www.howtogarden.net",
    "https://www.csa.gov",
    "https://www.foodandwaterwatch.org",
    "https://www.sustainablefoodtrust.org",
    "https://www.organicconsumers.org"
    ],
"Climate Policy": [
    "https://www.climate.gov",
    "https://www.unfccc.int",
    "https://www.c2es.org",
    "https://www.ipcc.ch",
    "https://www.wri.org",
    "https://www.worldbank.org/en/topic/climatechange",
    "https://www.climatepolicyinitiative.org",
    "https://www.nrdc.org/issues/climate-change",
    "https://www.carbontax.org",
    "https://www.greenpeace.org/usa/climate-change/",
    "https://www.climateaction.org",
    "https://www.climatehome.news",
    "https://www.eesi.org",
    "https://www.climate.gov.au",
    "https://www.oecd.org/environment/cc",
    "https://www.euractiv.com/topics/climate-policy/",
    "https://www.icc-gs.org",
    "https://www.ceres.org",
    "https://www.globalcarbonproject.org",
    "https://www.theclimategroup.org",
    "https://www.climateintegrity.org"
    ],
"Community Engagement": [
    "https://www.earthday.org",
    "https://www.climateinteractive.org",
    "https://www.350.org",
    "https://www.local-future.org",
    "https://www.resilience.org",
    "https://www.greencities.co",
    "https://www.climatestrike.org",
    "https://www.sierraclub.org",
    "https://www.communityenvironment.org",
    "https://www.sustainablecitiescollective.com",
    "https://www.citizensclimatelobby.org",
    "https://www.nwf.org/Our-Work/Our-Programs/Climate-Smart-Communities",
    "https://www.aclimateaction.org",
    "https://www.groundworkusa.org",
    "https://www.climatecouncil.org.au",
    "https://www.care.org",
    "https://www.greensolutions.org",
    "https://www.weforum.org/agenda/2020/09/community-engagement-climate-action/",
    "https://www.urbanecology.org",
    "https://www.civiclife.org"
    ],
"Biodiversity": [
    "https://www.worldwildlife.org",
    "https://www.conservation.org",
    "https://www.iucn.org",
    "https://www.biodiversity.org",
    "https://www.nature.org/en-us/about-us/where-we-work/priority-landscapes-and-seascapes/",
    "https://www.cbd.int",
    "https://www.wwf.org.uk/updates/biodiversity",
    "https://www.birdlife.org",
    "https://www.defenders.org",
    "https://www.nwf.org",
    "https://www.greenpeace.org/usa/biodiversity/",
    "https://www.aves.org",
    "https://www.biologicaldiversity.org",
    "https://www.biodiversitylibrary.org",
    "https://www.undp.org/sustainable-development-goals",
    "https://www.globalwildlife.org",
    "https://www.earthwatch.org",
    "https://www.rewilding.org",
    "https://www.ecologicalrestoration.ca",
    "https://www.terramarproject.org"
    ],
"Carbon Footprint Reduction": [
    "https://www.carbonfootprint.com",
    "https://www.carbontax.org",
    "https://www.nrdc.org/issues/carbon-footprint",
    "https://www.worldwildlife.org/pages/what-is-a-carbon-footprint",
    "https://www.epa.gov/ghgemissions/inventory-us-greenhouse-gas-emissions-and-sinks",
    "https://www.climate.gov/news-features/understanding-climate/what-carbon-footprint",
    "https://www.greenhousegasprotocol.org",
    "https://www.carbontrust.com",
    "https://www.carbonsavings.com",
    "https://www.nature.org/en-us/what-we-do/our-work/land-and-water/forest-carbon/",
    "https://www.sustainable.org",
    "https://www.greenbiz.com",
    "https://www.wwf.org.uk/updates/reducing-your-carbon-footprint",
    "https://www.recycling.com/reduce-your-carbon-footprint",
    "https://www.climatecare.org",
    "https://www.offsetters.ca",
    "https://www.carbonneutral.com",
    "https://www.carbonsolutions.com",
    "https://www.futureforests.com",
    "https://www.bbc.co.uk/news/science-environment-43905973"
    ],
"Climate Justice": [
    "https://www.climatejusticealliance.org",
    "https://www.globalclimateaction.org",
    "https://www.350.org/climate-justice",
    "https://www.climate.org",
    "https://www.motherjones.com/environment/2019/09/climate-justice-activism-fighting-for-our-planet/",
    "https://www.un.org/en/climatechange/what-is-climate-justice",
    "https://www.worldresourcesinstitute.org/our-work/topics/climate-justice",
    "https://www.jamesmartin.center/2021/04/12/climate-justice-and-the-problems-with-green-new-deal/",
    "https://www.greenpeace.org/usa/issues/climate-justice/",
    "https://www.cnbc.com/2021/04/25/climate-justice-what-is-it-and-why-does-it-matter.html",
    "https://www.nrdc.org/issues/climate-justice",
    "https://www.climatechangecommunity.org",
    "https://www.leonardoacademy.org/climate-justice/",
    "https://www.civilbeat.org/2021/01/a-primer-on-climate-justice-and-hawaii/",
    "https://www.renewableenergyworld.com/2021/05/17/the-path-to-climate-justice/",
    "https://www.brookings.edu/research/climate-justice-an-overview/",
    "https://www.polarisinstitute.org",
    "https://www.aclunc.org/news/climate-justice",
    "https://www.weact.org/our-work/climate-justice/",
    "https://www.equitytrust.org/what-is-climate-justice/"
    ],
"Sustainable Transportation": [
    "https://www.transportation.gov",
    "https://www.evtos.com",
    "https://www.c40.org",
    "https://www.sustainabletransportation.com",
    "https://www.apta.com",
    "https://www.wri.org/transportation",
    "https://www.gartner.com/en/newsroom/press-releases/2021-03-25-gartner-says-75-percent-of-organizations-are-investing-in-sustainable-transportation-initiatives",
    "https://www.trb.org/Main/Home.aspx",
    "https://www.euractiv.com/section/transport/news/eu-plan-for-sustainable-transportation-to-come-under-fire-in-parliament/",
    "https://www.ittfworld.com",
    "https://www.greve.org/transportation",
    "https://www.ucsusa.org/our-work/transportation",
    "https://www.iatp.org/sustainable-transportation",
    "https://www.sustainablecities.eu",
    "https://www.theclimategroup.org",
    "https://www.nrdc.org/issues/sustainable-transportation",
    "https://www.un.org/en/climatechange/sustainable-transportation",
    "https://www.cleantechnica.com/tag/sustainable-transportation/",
    "https://www.transportenvironment.org",
    "https://www.fhwa.dot.gov/environment/sustainable_transportation/",
    "https://www.planning.org/knowledgebase/sustainable-transportation/"
    ],
"Recycling and Circular Economy": [
    "https://www.euric-aisbl.eu",
    "https://www.recyclenow.com",
    "https://www.circulars.com",
    "https://www.circular-economy.com",
    "https://www.ellenmacarthurfoundation.org",
    "https://www.wrap.org.uk",
    "https://www.recyclingpartnership.org",
    "https://www.globalrecyclingday.com",
    "https://www.recyclingtoday.com",
    "https://www.worldbank.org/en/topic/circulareconomy",
    "https://www.nrdc.org/issues/recycling-and-waste",
    "https://www.cleantechnica.com/tag/circular-economy/",
    "https://www.pacificinstitute.org/resources/water-recycling-in-the-circular-economy/",
    "https://www.circulareconomy.com",
    "https://www.eco-business.com",
    "https://www.circulars.org",
    "https://www.circulareconomy.eu",
    "https://www.sustainablefoodtrust.org",
    "https://www.greenbiz.com/topic/circular-economy",
    "https://www.zerowastehome.com"
    ],
"Green Building Practices": [
    "https://www.usgbc.org",
    "https://www.greenbuildingadvisor.com",
    "https://www.breeam.com",
    "https://www.leedonline.com",
    "https://www.ashrae.org",
    "https://www.naiop.org",
    "https://www.gbci.org",
    "https://www.ecobuilding.org",
    "https://www.ecomii.com",
    "https://www.gartner.com/en/newsroom/press-releases/2021-09-14-sustainable-building-practices-accelerated-by-covid-19",
    "https://www.sustainablebuilding.org",
    "https://www.greenbuildingnews.com",
    "https://www.energy.gov/eere/buildings/zero-energy-buildings",
    "https://www.ghgprotocol.org",
    "https://www.ahrexpo.com",
    "https://www.sustainableconstruction.eu",
    "https://www.wellcertified.com",
    "https://www.igbc.in",
    "https://www.caba.org",
    "https://www.cleantechnica.com/tag/green-building/"
    ],
"Pollution Control": [
    "https://www.epa.gov/p2",
    "https://www.cleanair.org",
    "https://www.nrdc.org/issues/pollution",
    "https://www.who.int/health-topics/pollution",
    "https://www.nature.com/subjects/pollution",
    "https://www.oecd.org/env/pollution-control.htm",
    "https://www.cleantechnica.com/tag/pollution/",
    "https://www.greenpeace.org/usa/pollution/",
    "https://www.pollutionissues.com",
    "https://www.epa.gov/clean-air-act-overview",
    "https://www.fao.org/land-water/pollution/en/",
    "https://www.cdc.gov/nceh/lead/default.htm",
    "https://www.enviro.nj.gov",
    "https://www.airnow.gov",
    "https://www.cleanwateraction.org",
    "https://www.campbellclimate.com/pollution-control",
    "https://www.researchgate.net/publication/330329399_Pollution_Control_Measures",
    "https://www.sciencedirect.com/topics/earth-and-planetary-sciences/pollution-control",
    "https://www.nrdc.org/resources/pollution-facts-and-figures",
    "https://www.environmentalscience.org/pollution"
    ],
"Ecosystem Restoration": [
    "https://www.nature.org/en-us/what-we-do/our-work/conservation-approach/restoration/",
    "https://www.wwf.org.uk/what-we-do/land/ecosystem-restoration",
    "https://www.earthday.org/ecosystem-restoration/",
    "https://www.conservation.org/restoration",
    "https://www.iucn.org/theme/ecosystem-restoration",
    "https://www.restorationweek.org",
    "https://www.microscopemagazine.com/article/why-ecosystem-restoration-matters/",
    "https://www.unep.org/resources/report/unep-global-environmental-outlook-6",
    "https://www.greatergood.berkeley.edu/article/item/what_is_ecosystem_restoration",
    "https://www.nrcs.usda.gov/wps/portal/nrcs/main/national/landuse/forests/restoration/",
    "https://www.ecosystemrestorationcamps.org",
    "https://www.fao.org/ecosystem-restoration/en/",
    "https://www.rewilding.org/what-is-rewilding/",
    "https://www.sciencedirect.com/topics/earth-and-planetary-sciences/ecosystem-restoration",
    "https://www.nrdc.org/resources/what-is-ecosystem-restoration",
    "https://www.climate.gov/news-features/understanding-climate/why-ecosystem-restoration-matters",
    "https://www.restorationjournal.org",
    "https://www.worldresourcesinstitute.org/our-work/topics/forest-restoration",
    "https://www.ecomagazine.com/news/earth/2021/20-apr/5212-ecosystem-restoration-a-new-path-forward",
    "https://www.wwfindia.org/?196516/Ecosystem-Restoration"
    ],
"Climate Change Adaptation": [
    "https://www.unep.org/resources/adaptation-report",
    "https://www.worldbank.org/en/topic/climatechange",
    "https://www.climateadaptationplatform.com",
    "https://www.ipcc.ch/srccl/chapter/chapter-5/",
    "https://www.c40.org/climate-adaptation",
    "https://www.adaptation-undp.org",
    "https://www.nrdc.org/issues/climate-change-adaptation",
    "https://www.nature.com/articles/s41558-020-00905-x",
    "https://www.climate.gov/news-features/understanding-climate/climate-adaptation",
    "https://www.researchgate.net/publication/331224386_Climate_Change_Adaptation_and_Mitigation_in_Small_Island_Developing_States",
    "https://www.usaid.gov/climate/adaptation",
    "https://www.fao.org/climate-change/resources/adaptation/en/",
    "https://www.oecd.org/environment/cc/2050.htm",
    "https://www.cdc.gov/climateandhealth/effects/default.htm",
    "https://www.iucn.org/theme/climate-change",
    "https://www.climate.gov/teaching/lessons/adaptation-strategies",
    "https://www.theclimategroup.org/our-work/initiatives/adapt",
    "https://www.nap.edu/catalog/26209/advancing-the-science-of-climate-change-adaptation",
    "https://www.cabdirect.org/cabdirect/abstract/20183016562",
    "https://www.undp.org/publications/adaptation-climate-change",
    "https://www.wri.org/publication/understanding-climate-adaptation"
    ],
"Sustainable Fisheries": [
    "https://www.fao.org/fishery/en",
    "https://www.wcs.org",
    "https://www.msc.org",
    "https://www.fisheries.noaa.gov",
    "https://www.worldfishcenter.org",
    "https://www.seafoodwatch.org",
    "https://www.ifremer.fr/en",
    "https://www.iccat.int/en/",
    "https://www.iucn.org/theme/marine-and-polar/our-work/fisheries",
    "https://www.fisheryprogress.org",
    "https://www.fao.org/3/i9940e/i9940e.pdf",
    "https://www.marineconservation.org.au",
    "https://www.thefishsite.com",
    "https://www.sustainablefish.org",
    "https://www.sardines.info",
    "https://www.cites.org/eng/prog/Fisheries.html",
    "https://www.sustainablefisheriesuw.org",
    "https://www.nmfs.noaa.gov/sfa",
    "https://www.theoceancleanup.com",
    "https://www.marine.gov"
    ],
"Environmental Education": [
    "https://www.nwf.org",
    "https://www.naaee.org",
    "https://www.epa.gov/education",
    "https://www.edutopia.org/environmental-education",
    "https://www.environmentalscience.org/environmental-education",
    "https://www.greeneschools.org",
    "https://www.teachgreen.org",
    "https://www.eco-schools.org",
    "https://www.conservation.org/stories/educating-next-generation",
    "https://www.kids.gov/learn-about-the-environment",
    "https://www.schoolsustainability.org",
    "https://www.greenlearning.ca",
    "https://www.theeducationhub.org.nz",
    "https://www.ourplanet.com/en/education",
    "https://www.audubon.org/conservation/education",
    "https://www.earthday.org/education/",
    "https://www.environment.gov.au/education/index.html",
    "https://www.naturebridge.org",
    "https://www.nationalgeographic.org/education",
    "https://www.islandwood.org"
    ],
"Conservation of Natural Resources": [
    "https://www.nature.org/en-us/about-us/where-we-work/priority-landscapes/",
    "https://www.conservewildflowers.org",
    "https://www.nrdc.org/issues/conservation",
    "https://www.worldwildlife.org/initiatives/conservation",
    "https://www.eoearth.org/view/article/150507/",
    "https://www.usda.gov/topics/farming/conservation",
    "https://www.conservation.org",
    "https://www.sciencedirect.com/topics/earth-and-planetary-sciences/conservation-of-natural-resources",
    "https://www.iucn.org/theme/protected-areas",
    "https://www.epa.gov/sustainability",
    "https://www.oecd.org/environment/indicators-modelling-outlooks/greening-the-economy.htm",
    "https://www.fao.org/conservation-agriculture/en/",
    "https://www.conservation.org/stories/saving-nature",
    "https://www.nrcs.usda.gov/wps/portal/nrcs/main/national/home/",
    "https://www.worldbank.org/en/topic/environmental-sustainability",
    "https://www.researchgate.net/publication/330652279_Conservation_of_Natural_Resources",
    "https://www.nature.org/en-us/about-us/where-we-work/priority-places/",
    "https://www.usgs.gov/special-topics/water-science-school/science/conservation-natural-resources",
    "https://www.internationalconservation.org",
    "https://www.cbd.int"
    ],
"Smart Cities and Urban Planning": [
    "https://www.smartcities.gov",
    "https://www.c40.org",
    "https://www.urban.org",
    "https://www.itu.int/en/ITU-T/focusgroups/SmartCities/Pages/default.aspx",
    "https://www.smartcityexpo.com",
    "https://www.smartcitiesworld.net",
    "https://www.citylab.com",
    "https://www.worldbank.org/en/topic/smartcities",
    "https://www.weforum.org/agenda/2021/01/what-are-smart-cities/",
    "https://www.gartner.com/en/information-technology/glossary/smart-cities",
    "https://www.americanplanningassociation.org",
    "https://www.brookings.edu/research/smart-cities",
    "https://www.smartcitiesdive.com",
    "https://www.smartcitiesproject.com",
    "https://www.urbanland.uli.org",
    "https://www.sustainablecitiescollective.com",
    "https://www.intel.com/content/www/us/en/internet-of-things/solutions/smart-cities.html",
    "https://www.naiop.org/Research-and-Publications/Development-Opportunity-Reports/Smart-Cities",
    "https://www.nist.gov/engineering-laboratory/smart-cities",
    "https://www.citiesofthefuture.org",
    "https://www.local.gov.uk/topics/research-and-publications/smart-cities"
    ],
"Environmental Advocacy": [
    "https://www.environmentamerica.org",
    "https://www.greenpeace.org",
    "https://www.sierraclub.org",
    "https://www.nrdc.org",
    "https://www.cbf.org",
    "https://www.worldwildlife.org",
    "https://www.foe.org",
    "https://www.epa.gov",
    "https://www.conservation.org",
    "https://www.earthjustice.org",
    "https://www.audubon.org",
    "https://www.350.org",
    "https://www.peta.org",
    "https://www.nwf.org",
    "https://www.greenbuilding.org",
    "https://www.beyondpesticides.org",
    "https://www.nature.org/en-us/about-us/where-we-work/",
    "https://www.surfrider.org",
    "https://www.wilderness.org",
    "https://www.earthday.org",
    "https://www.climateactionnetwork.org"
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
    app = ApplicationBuilder().token(os.environ.get('7725726909:AAH2_zrjlGYwx1Pi9Z7tO9LVJWw7VMR6RHQ')).build()  # Use environment variable

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("feedback", feedback_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    app.run_polling()

if __name__ == '__main__':
    main()
