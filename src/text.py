TEXT = {
    "Frequency is Freedom": [
        """
“Frequency is freedom” is a phrase I learned when reading [Better Buses Better Cities](https://www.goodreads.com/en/book/show/44451608-better-buses-better-cities), and it has helped me articulate why I’ve felt a greater sense of freedom when I have lived and traveled abroad. Frequent transit service allowed me to go more places, to go places whenever I wanted to, and to still go places even when I was running late or forgot something (which seems to happen quite a bit). I spent less time waiting, so I got moving sooner and moved faster once I was on the go. I miss those freedoms, but I used to have those same freedoms here at home in Chicago.
        """,
        """
When ridership vanished at the beginning of the pandemic, the CTA was forced to cut service. Ridership plummetted from “1.4 million riders per day to a low of 225,000 riders per day”, [fare revenue dried up](https://www.chicagotribune.com/business/ct-biz-transportation-revenue-down-drivers-public-transit-20210325-u4yruab2gfei7myevume7kurim-story.html), and [the CTA ran fewer trains and buses](https://www.chicagotribune.com/business/ct-biz-cta-train-bus-schedule-wait-20211209-dd5aketifnefhnrtw6lsucleeq-story.html).¹ These days, as [the CTA struggles to hire enough bus drivers](https://blockclubchicago.org/2022/07/14/cta-leaders-vow-to-fix-unreliable-service-with-more-hiring-improved-train-and-bus-tracking/), service still runs less than scheduled. My own commute takes twice as long as it used to, which makes going into the office more of a pain. I miss the community of the office, but when I make the trek in I find it mostly empty because [my coworkers also all hate waiting forever for the bus or train](https://www.wsj.com/articles/dreaded-commute-to-the-city-is-keeping-offices-mostly-empty-11653989581).
        """,
    ],

    "How Often Does the Bus Come?": [
        """
Like nearly all transit agencies, the CTA publishes scheduled and real-time service data. While anyone who lives in the city knows that the bus never runs on schedule, we can look at this data to see the service the CTA intends to run. 
        """,
        """
Below is scheduled weekday service from the week of August 22nd, 2022, for two bus stops near my apartment. (I’ve filtered this data to only show service between 6 am and 10 pm, but the CTA does run buses and trains all night on many routes, including the 66 bus shown here.)
        """,
    ],

    "How Often Does the Bus Come? (II)": [
        """
I was shocked to see these charts. The shapes make sense to me (both buses have peaks at rush hour), but an average of 9 buses per hour for the Chicago Ave 66 bus is not at all what I experience. That’s one bus nearly every 6 and half minutes. I wish the bus ran that often, because how often the bus comes determines how long I’m stuck waiting for it.        """,
    ],

    "How Long Do You Wait For The Bus?": [
        """
Many things in the world of transportation are counterintuitive, such as how long you can expect to wait for the bus. If a bus arrives on average every ten minutes, you would be forgiven for thinking that the average time someone spends waiting for the bus is half that — five minutes. This would be the case _if_, and only if, the bus arrived like clockwork, every ten minutes. But it doesn’t: it arrives _on average_ every ten minutes, sometimes sooner, sometimes later. Surprisingly, the average time someone spends waiting for a bus like that is ten minutes.³
        """,
        """
To understand why, think about a university that advertises small class sizes. Tallying each class, the average may indeed be small, say thirty students. But not every class is that small. A few big freshman seminars may have hundreds of students.
        """,
        """
Since more students take those larger classes, the average number of students in their classes is actually much higher, because when choosing a student at random, you are more likely to get a student in a larger class. So, when a bus arrives at a certain frequency – sometimes shorter, sometimes longer – you are more likely to arrive at the stop during a longer period. This same paradox explains why [your friends have more friends than you](https://towardsdatascience.com/the-inspection-paradox-is-everywhere-2ef1c2e9d709#070e).
        """,
    ],

    "One Day of Simulated Bus Service": [
        """
Let’s simulate a bus and measure how long simulated people have to wait for it. Our simulated bus runs 24 hours a day and the little simulated people show up at all times (they work inside a computer and never get any time off). The chart zooms in to look at people and buses arriving at a stop between 10 a.m. and noon.
        """,
],

    "How Far Can I Go?": [
        """
How often the bus comes determines how far it can take me. While all buses that are at the [“mercy of the street”](https://www.wbez.org/stories/why-buses-arrive-in-bunches/4e768974-dd32-47f7-97e8-37951507e43d) will eventually bunch, buses that run more frequently bunch less.⁵ So, a bus that comes more often is more likely to come on time. (Bus bunching is when fast buses catch up to slow buses and, for a while, they travel together in a bunch. Riders wait and wait, no buses show, no buses show, and then several arrive at once.) Also, research from the US Department of Transportation has found that “a standard bus is able to remove 31 cars from the road”, so buses that come more often will sit in less traffic.⁶ But bunching and congestion aside, when a bus comes more often I spend less time waiting for it.        """,
        """
I want to use the CTA’s own data to measure how far I can go in a certain amount of time. To do that, I first need to map everywhere I can walk. What you see below is a map of everywhere I can walk within an hour of my apartment, which is near the intersection of Chicago and Damen.        """,
    ],

    "Geography": [
        """
The map above shows all walking routes surrounding my apartment. I find it quite beautiful how the highway to the east shows up almost like a river that I can only cross at certain spots. Chicago is quite a flat city with no hills or mountains to limit where we can build. Instead, our geography is defined by the transportation networks we build for ourselves.
        """,
    ],

    "How Far Can I Go with Public Transit?": [
        """
Now that we can walk, let’s walk to the bus, or, more realistically, let’s wait for the bus. From CTA schedules and our understanding of average wait times, we know how long we can expect to wait at each transit stop. We can then trace how far we can get on foot and public transit, including transfers, within a given amount of time. The maps below start from my apartment and consider weekday service from the week of August 22nd.
        """,
        """
This is my Chicago: the city the CTA makes accessible to me. I can get as east as the lake and as west as city limits. My reach northwest is expectedly defined by the blue line. North and south, I am confined by the limits of the bus, which peak in purple and blue. Since I live on the near west side, I have to go downtown before I can catch a train north or south. Doing that burns precious time. A friend of mine who lives in Ravenswood was surprised to see that his place isn’t on this map, but I wasn’t. I know to bike to his place for dinner, because the bus would take over an hour.
        """,
    ],

    "More Buses Take You More Places": [
        """
Truthfully, the map above is aspirational. It’s based off of the CTA’s published schedules, but the CTA has been running reduced service, sometimes as bad as running [half as many trains as the schedule says](https://blockclubchicago.org/2022/06/23/ghost-trains-and-buses-packed-platforms-35-alderpeople-want-city-council-hearing-on-deteriorating-cta-service/). That means waiting even longer and reaching even less.
        """,
        """
When public transit runs less often, our world gets smaller. Below are three thirty-minute trips from my apartment at increasing rates of service. The leftmost map shows 50% reduced service, the reality that my neighbors and I have been dealing with. The rightmost map shows a beautiful fantasy land where all buses and trains run twice as often as the schedule says.
        """,
    ],

"More Buses Take You More Places (II)": [
        """
These maps show how reduced service confines me to my neighborhood. I live a 15-minute walk to the closest L stop. When trains or buses run less than every 15 minutes, a 30-minute trip with public transit takes me barely further than just walking for 30 minutes. (Walking through Chicago's grid is what gives that first map it's diamond shape.)
        """,
        """
Below I explore longer trips and even more frequent service. Note how simple it would be to unlock more of the city. Tripling scheduled service doesn’t extend our reach much further than simply doubling it. We don’t have far to go, folks. We just need twice of everything!
        """,
        """
Twice as many trains and buses may sound like a lot to ask, but not if we view them as investments in the CTA’s resiliency. More transit riders means more fare revenue, and the best way to increase ridership is to run more buses and trains. Research from "157 US cities [has found] that increasing the frequency of service on current routes was about 20 percent more effective at increasing ridership than adding more routes."⁷ 
        """,
        """
I've never experienced true freedom like living somewhere where there's no need to check a bus schedule. Whenever you want to go somewhere, you simply get up and go. I want all Chicagoans to live that free.
        """
    ],

    "Better Bus Service": [
        """
The CTA is [hurting financially because of reduced ridership](https://experience.arcgis.com/experience/037eb95a8daa44f488e48d9afc09c38e), making it harder to run routes as often as advertised. This creates a vicious cycle, as worse service forces would-be riders to find other options. Many people think that those who are dependent upon the bus will take the bus no matter what because they have no other choice. Even the current head of the CTA, Dorval J. Carter has said, “The people who have to ride the CTA will ride the CTA.”⁷
        """,
        """
Those familiar with the transit geography of Chicago may notice in the maps above that it's not the L train that unlocks the city for me – it's the bus. The bus is often stigmatized as only for people who cannot afford a car, but that doesn’t measure up against reality. Research across the US has confirmed that bus ridership levels are a result of service quality.⁷ People choose the bus when they learn they can rely upon the bus. When they can’t, they – even people without a car – figure something else out.
        """,
        """
Something that I loved about Chicago pre-pandemic was that everyone, rich and poor, relied upon public transit. While friends from the suburbs would refuse to take the bus, no Chicagoan wasted time with that nonsense, because it was reliable and safe. [That’s no longer the case](https://blockclubchicago.org/2022/04/27/the-cta-boosted-unarmed-security-to-battle-violence-bad-behavior-on-trains-and-buses-but-riders-say-nothing-has-changed/), but the CTA can win us back. Kurt Luhrsen, vice president of bus operations for METRO, Houston’s transit agency, sums it up well: “You provide a good service, you’ll have customers. You don’t, you won't.”⁷
        """,
    ],

    "Draw Maps For Your City": [
        """
If you would like to recreate this project for your city, or develop it even further, please check out our [GitHub repo](https://github.com/ideo/frequency-is-freedom) or send me a note at jgambino@ideo.com.
        """,
    ],

    "Citations & Helpful References": [
    """
1. [CTA Leaders Vow To Fix Unreliable Service With More Hiring, Improved Train And Bus Tracking](https://blockclubchicago.org/2022/07/14/cta-leaders-vow-to-fix-unreliable-service-with-more-hiring-improved-train-and-bus-tracking/) from Block Club Chicago
1. [Dreaded Commute to the City Is Keeping Offices Mostly Empty](https://www.wsj.com/articles/dreaded-commute-to-the-city-is-keeping-offices-mostly-empty-11653989581) from The Wall Street Journal
1. [The Waiting Time Paradox, or, Why Is My Bus Always Late?](https://jakevdp.github.io/blog/2018/09/13/waiting-time-paradox/) by Jake VanderPlas
1. [The Inspection Paradox is Everywhere](https://towardsdatascience.com/the-inspection-paradox-is-everywhere-2ef1c2e9d709) by Allen Downey
1. [Why buses arrive in bunches](https://www.wbez.org/stories/why-buses-arrive-in-bunches/4e768974-dd32-47f7-97e8-37951507e43d) from WBEZ
1. [How the Chicago region’s transit system is going even greener](https://blog.rtachicago.org/2022/04/20/how-the-chicago-regions-transit-system-is-going-even-greener/) from the RTA
1. [Better Buses, Better Cities: How to Plan, Run, and Win the Fight for Effective Transit](https://www.goodreads.com/en/book/show/44451608-better-buses-better-cities) by Steven Higashide
1. [Isochrone Maps with OSMnx + Python](https://geoffboeing.com/2017/08/isochrone-maps-osmnx-python/) by Geoff Boeing
1. [The Mobility Database](https://database.mobilitydata.org/) and [GTFS Schedule Reference](https://gtfs.org/schedule/reference/)
1. [Isochrone Maps with R and OpenTripPlanner](https://xang1234.github.io/isochrone/) by David Ten, for his very helpful diagram of the GTFS schema.
1. And lastly, a big thank you to [all my lovely coworkers](https://www.ideo.com/jobs) who helped with this project. You're brilliant and beautiful.
    """,
]

}