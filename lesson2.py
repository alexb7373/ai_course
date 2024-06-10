#!/usr/bin/env python
# coding: utf-8

# In[3]:


import langchain
from langchain.llms import Ollama
from langchain_openai import ChatOpenAI
import json, re


# In[4]:


# https://levelup.gitconnected.com/introduction-to-ollama-part-1-1156f9563b8d
# https://levelup.gitconnected.com/introduction-to-ollama-part-2-e8516105f600
# https://ollama.com/library
# https://stackoverflow.com/questions/77550506/what-is-the-right-way-to-do-system-prompting-with-ollama-in-langchain-using-pyth
# https://python.langchain.com/v0.2/docs/integrations/chat/openai/


# In[5]:


# ollama list
# NAME            ID              SIZE    MODIFIED
# aya:latest      7ef8c4942023    4.8 GB  3 hours ago
# phi3:latest     64c1188f2485    2.4 GB  3 hours ago
# llama3:latest   365c0bd3c000    4.7 GB  3 hours ago
# mistral:latest  2ae6f6dd7a3d    4.1 GB  4 hours ago


# In[ ]:





# In[6]:


llm = None
model = None


# In[7]:


with open('../../openai_api_key.txt') as f:
    openai_api_key = f.read()


# In[9]:


with open('swagger_petstore.json') as f:
    swagger_api_spec = json.load(f)


# In[15]:


messages = [
	[
	("human","If we lay 5 shirts out in the sun, it takes 4 hours for the shirts to dry. How long does it take to dry 20 shirt? Explain the reasoning step by step.")
	],
	[
	("human","How many words are your response to this prompt?")
	],
	[
	("human","There are 3 killers in the room. Someone enters the room and kills one of them. Nobody leaves the room. How many killers are left in the room? Explain the reasoning step by step.")
	],
	[
	("human","John and Mark are in a room with a ball, a basket and a box. John puts the ball in the box, then leaves for work. While John is away, Mark puts the ball in the basket, and then leaves for school. They both come back together later in the day, and they do not know what happened in the room after each of them leaves the room. Where do they think the ball is?")
	],
	[
	("system", "Talk to me in style of Joe Rogan."),
	("human", "What do you think about Jiu jitsu?")
	],
	[
	("system", "You are Joe Rogan, posessing his knowledge and behaving like him."),
	("human", "What is your name?"),
	("human", "Do you like MMA?"),
	("human", "Where do you live?"),
	("human", "Have you ever done any standup comedy?"),
	("human", "Do you have kid?"),
	("human", "Tell me a standup comedy bit about ... yourself")
	],
	[
	("human", """
	Goal:
Implement a snake game in python.
User should be able to use arrows to move with snake.
Snake should grow if eats point.
Snake should die if move from screen.
Snake should die if hit himself .
	"""),
	("human","Create a game snake in Python. Write a code, so I can copy paste it and run it.")
	],
	[
	("system", "you are a software developer, implementing an API. You are supplied with a swagger API spec."),
	("human", "Swagger API spec: ===\n"+str(swagger_api_spec)+"\n==="),
	("human", "For given swagger file, generate a request that places a new order for a pet."),
	("human", "For given swagger file, generate a request that places a new order for a pet. Return clean code in Python, so we can copy paste it and run it.")
	],
	[
	("system", "you are a software programming consultant"),
	("human", """You are given a definition of finctions - in the JSON that follows.
	If user question can be answered by some of the functions in the array. 
Return as answer JSON object that contains name of the function and request that should be send to the function.
If user question cannot be answered by any function, answer as you would do normaly. 
	```JSON
[
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get the stock price of an array of stocks",
            "parameters": {
                "type": "object",
                "properties": {
                    "names": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "An array of stocks"
                    }
                },
                "required": [
                    "names"
                ]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_big_stocks",
            "description": "Get the names of the largest N stocks by market cap",
            "parameters": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "integer",
                        "description": "The number of largest stocks to get the names of, e.g. 25"
                    },
                    "region": {
                        "type": "string",
                        "description": "The region to consider, can be \"US\" or \"World\"."
                    }
                },
                "required": [
                    "number"
                ]
            }
        }
    }
]
```
	"""),
	("human", "Question: How expensive is Microsoft?")
	],
	[
	("human","What is Autogen?")
	],
	[
	("human","Classify the sentiment of the following review: 'The interface is very intuitive, but the API documentation is lacking.")
	],
	[
	("human", """You are given a couple of sample prompts, with correct answers to them:
Review: "Great performance, easy to install." Classification: Positive
Review: "The installation was easy, but the software has too many bugs." Classification: Negative
Review: "Good features, but the manual is useless." Classification: Negative
	"""),
	("human","""Review: 'The interface is very intuitive, but the API documentation is lacking.' Classification: ?" """)
	],
	[
	("system", "You are Quentin Tarantino, communicate as he would."),
	("human", "Hey who are you?")
	],
    [
	("system","You are AI assistant."),
	("human", """What are the best bits in this standup?
===context===
[indistinct chattering] [faint laughter]
[audience cheering and applauding]
Oh! What the fuck, Boston? Goddamn! Thank you. It’s good to be here. Good to be back. Fuck! I love it. Goddamn it! Good to see happy people… having a good time. It’s a tense world we’re living in today. You got a president that’s threatening to fight an ex-vice president. [laughter] You pay attention to that shit? It’s a couple weeks ago on Twitter. Donald Trump said that if he fought Joe Biden, Joe Biden would go down fast and hard. [laughter] I want to get in his ear. I’ll be like, “Let’s make this happen, bro.”
[laughter]
There’s money on the table.
I’ll commentate for free
[laughter] No rules, grow your nails out, wear a diaper.
No clothes. To the death.
[laughter] Fuck it. Let’s bring this thing totally down. Seems like every day you turn on the news, more and more crazy shit. When are we going to realize we shouldn’t have a fucking president? It’s a ridiculous idea to have a popularity contest to see who controls everything. Because if you could go back in time and grab Thomas Jefferson and bring him to 2018… his first question would be… “You guys didn’t write any new shit? [laughter]
Dude, I wrote that with a feather.
[laughter] I did it by fire! That’s the only way I could see what I was writing! You lazy fucks! You guys have phones in your pockets and spaceships! ‘But the wisdom of the scroll shall not be adjusted.’ What the fuck does that even mean? Who told you that, bro?” [laughter] We always like to say, “The long, great history of the United States.” Listen, that’s not real. The United States was founded in 1776. People live to be a hundred. That’s three people ago. [laughter] You’re like, “Is he right?” Yeah! The Fear Factor guy just hit you with a fucking math quiz! [laughter] Three people ago! Listen to me, you’re not going to get this from teachers. We used to be monkeys, and we found mushrooms, and now we’re different. And it’s real, real recent. [laughter] No one knows what’s going on. Three people ago, slave owners made boats out of trees, and used the power of the wind to drift across the ocean. They didn’t have a YouTube video to watch first. They didn’t talk to a travel agent. You know what they had? A drawing.
Some guy went there and drew it.
[laughter] Like, “Are you sure that’s what you saw?” “That’s what I saw! You callin’ me a liar?” And they had a gunfight in the dirt streets. They were fucking savages just three people ago. They took their baby and jumped on a boat and floated across the fucking ocean with their kids. Animals. That’s us. It just happened. Real recent! “I just never saw Trump coming.” Well, you don’t pay attention to trends. We have a very clear trend in this country. We try one person as president, and the next person has to be completely opposite. ‘Cause no one can do the job correctly. So we let someone try it and we’re like, “He fucked it up.” We go with this guy who’s totally different, who’s got our interests in mind. And we always do the same thing. We go right, left, dumb, smart. We give everybody a chance.
[laughter]
We go Clinton, Bush. Then we go Bush, Obama. Obama, Trump. We just got out of a long-term relationship with a very boring but sensible person, and now we’re dating a whore.
[laughter]
[cheers and applause] All right? She’s got fake hair. She’s racist. She’s always lying. We don’t care! We’re not trying to start a family, we just want to run red lights and fuck.
[laughter]
All right? [applause] For real. We don’t know what we’re doing. If this country was a person, we’d be on coke, driving a yellow Corvette, singing Mötley Crüe songs in front of our ex’s house. [laughter]
We’re going crazy!
[laughter] “Well, it would have been so much better if Hillary won.” [moans]
[audience cheers]
“Oh, we got so close!” “Oh! We almost had a woman!” Oh, girls, relax. I think a woman can be president. But let’s not use a lying old lady who faints a lot. [laughter] I think you can do better. It’s not that I don’t think a woman can be president. I’m fucking sure a woman can fuck it up just as bad as the men that fucked it up. No one’s going to do it right. But if Hillary Clinton was my own mom, I’d be like, “Mom! You can’t be president. You can’t stand up fast.” [laughter] “I’ll show you! One ring to rule them all…” [groans] [laughter and applause]
[in a woman’s voice] “Oh, you’re sexist! I see, you’re sexist! As well as short. You’re fucking sexist!” Ugh! Defuse my point of view. I am sexist. But I’m sexist against men. I decided during this whole Harvey Weinstein thing. This is why. That’s when I realized I was… I had some suspicions… that I might be sexist before that. [laughter] That’s when I really decided. ‘Cause what Harvey Weinstein did, it was fucking terrible. Can you imagine being an actress? You gotta fuck that guy in order to make it. Like, ugh. What a horrible choice. Like, what a terrible position to be in! “This is the only way?” That sucks. That’s fucking… That’s criminal. I think that guy’s a piece of shit. I think he should be punished.
But!
[laughter] If he had done the exact same thing to men, I wouldn’t give a fuck. [laughter] I wouldn’t even be slightly upset. [laughter] If I was reading the morning paper and I read a story about a bunch of dudes who let Harvey Weinstein fuck ’em…
[laughter] -so they could be in superhero movies… [laughter] I’d read that, I’d go, “Ha-ha!” [laughter] What else? What else is happening? [chuckles] [laughter and applause]
I wouldn’t be clamoring for justice.
[audience member] Woo! [laughter] If Harvey Weinstein was a woman who looked like Harvey Weinstein… [laughter] and she did the exact same shit to men, my only question would be, “Hey! How bad you want to be Batman? [laughter and applause] How long is it going to take, bro? You could wait tables in this town for 20 years and never catch a break. Or you give the nice lady what she wants. [laughter] Jude Law is in the waiting room and he’s wearing a lobster bib.
You tell me…
[laughter] if you want to be a winner. [laughter] They don’t fucking give Ferraris away, son! They make ’em by hand.” [laughter] If Harvey Weinstein propositioned my daughter and offered her a movie role in exchange for sex, I, like every other parent in this room, would want to fuck him up. But if Harvina Weinstein… [laughter] came to my son with a solid contract… [laughter] I’d be like, “Dude, you’re gonna be Batman. [laughter and applause] Yes, you are.
[cheers and applause]
[whistles] Hey, no crying! Batman doesn’t cry! Come on!” “Your own son? Really?” Jaaaaa. What’s the worst thing that can happen? It’d be a harder job. It’d be hard to please Harvina. [laughter] Right? Rich old lady, it’s probably real hard to make ’em come. You gotta make eye contact, you gotta lock in with them. They got to know you’re involved in this project. Right? Rich old ladies are probably super skeptical. [grunts] [laughter] Look. Always, always maintain eye contact. That wouldn’t be the hard part. The hard part is, when you go down on Harvina, she likes to rest her fat gut on your forehead. And the sweat! The sweat gets in your eyes! And it stings like sunscreen! But you gotta keep ’em open ’cause you want a Ferrari! Aah! Aah! [laughter] Nobody cares. Nobody cares about boys that have to eat pussy. No one cares. [laughter] We’re all sexist against men. No one cares. No one feels bad. [faint laughter] “How’d you get that car?” “Man, I had to eat pussy for it.” “You gonna be okay?” [laughter] Feel bad for you.
[Joe laughs]
[laughter] Look, I get it. Men are gross, ladies. I’m on your side. My favorite example of the difference between the way men and women are treated was always old school Fox News. I used to watch it without the sound on, so it’s almost like watching a wildlife program, just watch them move around. I was watching it once and Megyn Kelly was on, and she was on with Bill O’Reilly. They were right next to each other, so I assumed they were in the same climate. But Bill O’Reilly was dressed like there was a chill in the air. He had a jacket on, a shirt, a tie, and pants. And Megyn Kelly was wearing what would best be described as a vagina curtain. [laughter] Not a good curtain either. Not like one of those Vegas curtains that lets you sleep in late. No, no, no. No, this curtain is like that curtain that sits over Grandma’s kitchen sink.
You know that one?
[laughter] Kind of flutters in the breeze. You could always see the yard. You know that one? And Megyn Kelly’s on TV with smooth, slippery skin that doesn’t exist in nature outside the dolphin community. [laughter] You’d see her toes. You’d see her feet and her toes. She could just kick off her shoes and there’s a Dorito-sized piece of cloth keeping you from the greatest show on earth. And it’s right there. She knows it’s right there, you know it’s right there and no one’s saying a fucking word. And if she disagrees with you, she’ll adjust the curtain and switch her legs. Hmm.
[faint chuckles]
Hmm. Nobody says nothing. If I was talking to a dude… and he didn’t have any pants on… [laughter] and he kept switching his legs back and forth… I’d be like, “Hey, man. Are we cool? [laughter] Where the fuck are the rest of your clothes? Why you so itchy? Where’d you get those shoes?” No one says shit while Megyn Kelly’s over there trying to start a fake tan fire in her pussy. [laughter] [blows air] [a clap, laughter] It’s weird. I’m not saying there’s anything wrong with it, but it’s weird. She doesn’t have any sleeves on. Where are your sleeves? [laughter] That’s not weird? It’s not weird, it’s strange. “I want you to respect me.” I want to respect you, but you’re half-naked and I want to fuck you, so I’m confused. I don’t know what to do. I’m thinking of saying anything you want. Whatever you want me to say, I’ll say it. I want you to like me more. That’s the problem with a woman that’s that beautiful and super smart. You know she’s smarter than you. She’s a lawyer. She never says “um,” she’s smart as fuck. [laughter] And she’s really, really, really pretty, and she doesn’t have a lot of clothes on.
She’s gonna get her way. All right?
[laughter] You won’t tell her to go fuck herself. You’ve to be super secure to do that. And you can see some of her tit. [laughter] That’s weird, right? If I came here like this, you’d be like, “Joe, what the fuck are you doing, man?” [laughter] Right, but if Megyn Kelly’s on TV, “Oh, she’s just got a cute shirt on. It’s just cute. It’s cute.” You could see some tit. You could see some middle tit. You might even see some side tit if you catch… if she’s pointing at something, she might just… “I didn’t even know you were looking at my side tit.” She’ll just pretend. But long as you don’t show the dirty, dirty dark skin.
[groans] There it is!
[cheers and laughter] The sensitive, forbidden skin! Put it away! It’s not for strangers! [laughter] That’s fucking strange, ladies. Listen, don’t listen to me. I’m a moron. Wear what you’re wearing, it looks great, but it’s weird. You can show some of a sex organ. What if that was the case with dudes? What if we had a window in our pants, we could just see the shaft? [laughter] Right? Just the shaft. [laughter] You can’t see the head of my dick, I’m not a creep. [laughter] Okay? Just a little side dick. [laughter] You have cleavage, we have tubage, it’s no big deal. It’s whatever. Just showing a little tubage. Why do I dress like that? To look cute for my friends. Okay? God! You’re so fucking jealous.
I need to get a sip of water. Excuse me for a moment here. [Joe clears throat] I probably should’ve taken this onstage with me, but I’m trying to be cool. That’s that cotton mouth, son. [laughter] [sniffs, clears throat] Woo! [cheers and applause] Yeah, you guys are legal now. I grew up here. We used to hide in the bushes and smoke weed. Ridiculous. Hiding from cops that are now getting high. Going, “What do I do to all those fucking kids? Hoo-hoo-hoo.” [laughter] The real problem is the laws. And Massachusetts finally has good laws.
We’ll be able to understand…
[cheers and applause] what pot actually is. Florida’s got the craziest laws, ’cause Florida’s trying to protect their pain pill industry. So in Florida, they make it so illegal, this is one of the things they do in Florida: they hire undercover cops to pretend to be high school students. Specifically a hot woman. They hired a 25-year-old hot woman to pretend to be a high school student, flirt with boys, get those boys to sell her weed, and then arrest them. [faint laughter] I don’t like to use the word “cunt.” [laughter] When I use it, I want it to mean something. That’s a cunt. That lady’s a piece of… fucking human garbage.
You fucking asshole. Here’s the thing.
[laughter] Not only is it not fair, that is one of the most sexist stories you’ll ever hear. Here’s why it’s sexist. It’s sexist against boys. Here’s why. You could never imagine that story if the genders were reversed. If you found out that a 25-year-old man was throwing dick at your 17-year-old daughter, and he talked her into selling him weed, and then he arrested her, we would light that motherfucker on fire in the street. Right? [cheers and applause] But if it was my own son who got arrested by that cop, I’d be like, “How’d it go? [laughter] Tell me what happened. Record? You’re worried about your record? You got a story, dude. You got a… You’re the first guy ever to get arrested by an undercover cop you thought was his girlfriend. [laughter] That’s a fucking hell of a story.” Some people are, like, hard asses about it like, “Shoulda known better. He’s almost 18.” Yeah, but he’s almost 16 too. [laughter] Which is almost 15. That’s like a little kid. Do you remember what you were like when you were 17? You didn’t know what the fuck was going on. And this kid wasn’t even a drug dealer. This kid, it’s not like he got caught. No, this kid was a straight-A student that thought he was getting pot for his girlfriend. He even tried to give it to her. She wouldn’t accept it. She wanted to give him money, so she could arrest him. But he had to know, he was a smart kid. He had to know. He had to know something was off. ‘Cause here’s what it’s like: a 25-year-old woman is not the same as a 17-year-old girl. They look similar, but they’re not the same. Here’s what it’s like: I had this dog once that I got from the pound. [laughter] You know how you get a dog… “Are you comparing women to dogs?” No! [laughter] You’ll see. [laughter] The dog, she was a sweetheart of a dog, but she had been the pound too long, she was real sketchy. And I would bring her around other dogs, and, like, when a dog has been in the pound, like, every other dog they think is going to take their food or take their bed. So I take it to the dog park, and she’d see dogs and go, “Fuck off! Fuck off!” And every dog would be like, “Whoa, Jesus.” [laughter] That’s how she acted with every single dog till one day, one day I brought her to the dog park and somebody brought a wolf. Some fucking hippie asshole with wooden beads on, wearing sandals, this motherfucker brought a thing that eats dogs into a cage filled with dogs! [laughter] My dog looked at that wolf and looked at me and went, “That’s not a fucking dog! Aah!” [laughter] She knew. I don’t know how she knew. She didn’t grow up in Alaska. She wasn’t a Montana dog. How the fuck did she know? But she knew. Somehow. Somehow. That had to be what it was like when that 17-year-old boy was around that 25-year-old woman. Like, “Um, where’d you go to school?
Unh? Hmm?”
[laughter] She’s like touching him. [groaning] ‘Cause 17-year-old girls don’t sound anything like 25-year-old women. You ever talk to a 17-year-old kid? They don’t know what the fuck they’re saying. They’re basically just practicing talking. [laughter] They’ve only been talking for, like, a few years. [laughter] They don’t know how to make shit sound good. They’re like, “Have you heard the new Drake song? It’s so fire!” You’re like… [groaning] Argh! What the fuck did you do to my ears? Meanwhile the 25-year-old cop’s like, “Let’s go back to my house, smoke some pot, and snuggle.” That kid’s like… “You have a house? [laughter]
How the fuck did you get a house?
[laughter] Your dumb friends are like, “She saves, bro. [laughter] My cousin did it, my cousin bought a house.” Kids are always lying. 17-year-old kids. “Yeah, my cousin bought three houses by the time he was four.” What? Four? [laughter] Seventeen. “You should know better.” You know how crazy that is to say? That is a short amount of time on this planet, seventeen years old. And it’s a confusing time. Maybe one of the most confusing times ever for a boy, because your life is a certain way for 13 years, and then you start getting uncontrollable boners right around 13 years in. For 13 years you think you got life mapped out. “I get life, you do what you want, you kind of have a good time. You ride your bike and you play your games, hang out with your buddies.” And then suddenly two years later you’re waking up going,
[screaming] “What do you want from me?”
[laughter] And your dick’s like… [groaning] Every day. Every day. Confusion. “Do I love you?” [laughter] “What are you gonna do for a living, bro?” Another thing you get when you’re 17. “What are you gonna do? You’re almost a man. Be a loser?” “I don’t know.” And then you see, you see around you all these people that are chasing bullshit. Material possessions and nonsense lives, doing things they hate and getting stuck in a rut. You don’t want it to be you and you don’t know how to get out of that. And everybody’s confused and everybody’s like, “Bro, what are you gonna do for a living?” I don’t know! I don’t know. Just get together with your friends and try to figure life out. Unwind, hang out, smoke a little joint. Like, ‘Dude… [snorts] I think my girlfriend’s a cop.” [laughter] [cheers and applause] I’m like, “Dude, you’re paranoid. Trust me, it’s the weed. There’s no way.” Meanwhile, he was right. Poor little fuck. Nobody cares. ‘Cause nobody cares about boys. Why? Listen, don’t “aw.” It’s okay. We’re running shit. [laughter] It’s the balance of power.
Look, it’s… it’s all for good. So much tension. ‘Cause, like, this is a new time for jokes too, because everything I say on this Netflix special is going to get me in trouble, but I… I knew coming in. But I want to explain to people if they’re mad at me. Talk to me offstage, I’m super reasonable. But I say shit I don’t mean ’cause it’s funny. Like, people should get that but they don’t get that, not in 2018. Everybody wants to write it down and make it literal. “This is exactly what he said, here’s a quote.” “Oh, hate! Let’s end the hate! Enh!” [applause] And people are way more sensitive now. Because of the Internet, everybody has an opinion and they can all express it, when that’s not really necessary for some folk. Some folks, their opinion’s not that good. They should… keep it to themselves. But today, anybody can express opinions. I’ve gotten death threats for shit I don’t even remember saying. Like, I did a podcast with Tony Hinchcliffe, and apparently I said I thought pro wrestling was gay. [laughter]
I don’t even remember saying it.
[laughter] But I got off the podcast and I checked my Twitter, and the fucking hurricane of misspelled hate messages that came my way. I was like, “Aah!” What have I done? [laughter] I didn’t even mean what I said. It was just a funny thing to say in that moment ’cause he’s so into it. I’m like, “It’s gay.” It’s funny to say! [laughter] “No, it’s not ever funny to say.” Well, you don’t hang out with my friends. So I don’t know what the fuck to tell you. “Well, you’re a homophobic piece of shit! I wouldn’t hang out with your friends!” That’s not true. Here’s where you’re wrong. I… ‘Cause people tell you that you shouldn’t say something’s gay. But I love gay people. I’ve no problem with gay people. I’m happy they’re a real thing. I really am. I like it, mix it up. Who gives a shit? [laughter] So if you don’t like me calling things gay, then what word would you like me to use to describe gay shit? [laughter and applause] What are we doing here, man? There’s certain noises we can’t make with our face anymore? You know, I think the same fucking thing, right? [laughter] Gay’s not negative. It’s just gay. Okay? There’s certain things… [chuckles] There’s certain things that are gay that have nothing to do with men having sex with each other. Like musicals.
[laughter]
Right? No one knows why. They’re just gay. Men wearing pearls, gay as fuck. [laughter] It’s not a negative. And I don’t really hate pro wrestling. I was just talking shit. Like, when I was a kid, I loved Jimmy “The Superfly” Snuka, and Bob Backlund, and Hulk Hogan, and I love The Rock. I go to his Twitter page every day for inspiration. And who’s not a fan of Ric Flair? [audience] Woo!
We didn’t rehearse that!
[laughter] You knew what to do! That man has an exuberant noise attached to his name. That’s one of the most American things of all time. Right? I was just talking shit. That’s all it was. So Tony goes, “Listen, if you just watch pro wrestling with me, you’ll love it, and you’ll become a fan.” I’m like, “All right, dude. Turn it on.” He turns it on! I see a guy with shaved legs, wearing Speedos, with knee-high leather boots on, and he’s holding another guy down. But not really. [laughter] The guy’s like, “I can’t even get up.” And the guy he’s holding down is wearing a leather mask!
I’m like, “What the fuck, Tony!
[laughter] Have you watched this with a critical eye?” [uncontrollable laughter] I’m not saying it’s gay. But let’s just be honest. Everywhere else on the planet, other than that ring… [laughter] Everywhere else on Earth, when a dude shows up shirtless, wearing a leather mask and Speedos… he’s there to suck dicks. Okay?
Period.
[cheers and applause] I don’t care what you tell the cops. That guy knew what the fuck he was doing. So there’s going to be people mad at me for that, but I just want you to know, for a bunch of things. Here’s what’s really important. And I can’t believe you’ve to do this, but in 2018 you’ve to do this. You’ve to say a joke and then you go, “Hey, that’s not…” This is what I really feel. This… this is what I really feel. There’s nothing wrong… I don’t want anybody thinking I’m a bigot. There’s nothing wrong with being gay, nothing, and there’s nothing wrong with being a fan of pro wrestling. [laughter] But it’s the same thing. [laughter and applause] To me. I respect both of them. I think both of them are amazing. I’m super happy.
I’ve had some other death threats this year. I, uh… [chuckles] …put a poster up, put a picture up on Instagram of some deer meat, and I wrote, “This is some meat from a deer that liked to kick babies and was about to join ISIS.” [laughter] I was feeling real good about that post. Then I got cocky and I wrote hashtag #vegan and that’s where I fucked up. [laughter] Ooh! That wasn’t worth it. That didn’t feel good. Oh! The hate, the anger! Never in my life have I encountered such a ruthless, vicious group of kind, compassionate people… [laughter] as I have in that fucking hashtag #vegan group. [faint laughter] These vegans that are vegans for good reasons, folks, but the problem with vegans is the problem with every single group of human beings. If you get a group of 100 people, just pick a random 100 people, what are the odds that one of them is a fucking idiot? It’s 100%. We nerf all the sharp edges in this world and we let dummies survive. There’s no wolves running through our streets. It’s 100% that one out of 100 is a fucking idiot. Some of those are vegans, and this is how it works: if you got a group and you don’t have to take a test to get in there, some of them are in there for the right reasons. Most vegans are vegans ’cause they’re kind people. They don’t want anything to die so they can live. And those people are heroes, ’cause they’re always tired, they’re cranky, their health’s all fucked up. They’re doing it for all the right reasons. But then there’s vegans who are really only vegans ’cause Scientology didn’t find them first.
[laughter and applause]
-Okay? You know. Everybody knows certain vegans that would have joined the Taliban if they took the wrong flight, all right? They’re fucking dipshits. Those guys always have “vegan” in their name. It’s always like “vegan warrior.” They just start eating plants and start talking shit. They joined a gang. It’s a plant-based gang. [hysterical laughter] I don’t argue with these people but I do when they say something totally crazy to me. I will check their profile, see what they’re interested in. And this one lady said something really fucked up. She wrote me, she goes, “I hope animals eat your children in front of you. I hope everyone you know gets cancer. I hope you die in your mother’s arms.” And I’m like, “Well. [laughter] What’s this healthy lady up to?” [laughter] [laughs] So I go… I go to her fucking page. She has a bunch of hashtags, right? Normal ones like hashtag #vegan, hashtag #crueltyfree, and then I seen one that I’ve never seen before. It says hashtag #vegancat
[faint laughter]
[Joe sighs] I check my watch. It’s 1:00 in the morning, I’m like, “Fuck, do I click this?” [laughter] I’m like, “I should just go to bed, right? I should just go to sleep. I shouldn’t do this. I should have some herbal tea and read a book.” And there’s the other part of your brain like, “Shut up, pussy. Click it. Come on! Come on!” I always listen to that part. That’s the secret to my success, I always listen… [chuckles] “Come on, pussy! Come on!” I click it. I’m hoping… This is what I’m hoping. I’m hoping hashtag #vegancat… I’m hoping what that is is, like, a support group. [laughter] Right? Like, we all have friends that are vegans that also have cats. You go over to their house and you’re like, “So why are you vegan again?” “Well, I just don’t think it’s our right to decide that an animal should live or die.” And then they open up a fat can of murder and give it to that little fucking psychopath that they live with. And you’re like, “Hey. [chuckles] Hey, man. What’s in that fucking can? What are you doing?” “Well, he’s a carnivore but I’m an herbivore.” If you are a vegan with a pet cat, that’s like being a doctor with a pet vampire.
[laughter]
Pick a team, fuck face. What are you doing? You live with a murderer! Okay? If you love animals, just shoot that cat right in the fucking head. That thing eats 200 animals a year. [laughter] That is what I was hoping. That’s what I was hoping hashtag #vegancat meant. Oh! But no. No. #vegancat is a whole fucking community of people who think it’s a good idea to feed your cat salad. [laughter] Now, before I go any further, it’s very important that I be completely truthful to you, ’cause people call you out all the time. It’s always some guy. “Actually… Actually you can feed your cat a vegan diet.” They do that little cunt nod. You know that thing that people do? [laughter] They tell you something and then… Oh, is that the worst? Even if they’re right, you’re like, “Fuck you and your facts. This fucking face thing you’re doing.” But he’s right. You can… feed your cat a vegan diet if you don’t mind them going blind… and dying young. “Is he serious?” Yeah, I’m fucking serious. You will, after this show, go on your phone and check out hashtag #vegancat, and you will be treated to a collection of pets that look like they live in a house with a gas leak. [laughter and applause] Every fucking cat is like, “When is the real food coming? What the fuck is…” They’re all lying down! I’m not joking! Every fucking cat. You’re gonna go, “He’s right!” They’re all lying down! All of ’em! And they die young! Really fucking young! They take pictures, these fucking psychos. “RIP Tabby! We had five amazing years together!” The cat’s eyes are milky, its legs are stiff. It’s like… “What is this lady feeding me? Where’s the real food, bitch?” It’s a cat! You got to feed it cat food! “Hashtag #crueltyfree.” Tell that to your blind, dead cat, you fucking crazy asshole! -It’s a cat! Okay?
[whistles and cheers and applause] It doesn’t want to eat mashed potatoes! It makes us uncomfortable that something would want to kill something because what if someone wants to kill us? I don’t want that. That’s what it is. It’s just weird panic that we have about our own mortality. But it’s a real simple system. If this comes up in an argument, feel free to use this. This is how it works: Green shit grows out of the ground, dumb shit eats the green shit, mean shit kills the dumb shit. That’s your cat. That’s why you don’t have to hack your way through a river of bunny rabbits to get your fucking Prius every morning. Okay? You can’t feed that thing cranberries. [laughter] “We went to see Joe Rogan and he hates gays and cats. I am currently blogging about it.” [laughter] None of this is true. I love gay people and I have cats, and my cats are fluffy, which is gay. [laughter] I have gay things that I love. I listened to Miley Cyrus music right before I got onstage tonight. There’s plenty of gay things I love. I have those fluffy, those Monsanto, GMO cats. You ever see those cats? Like, how the fuck did that turn into that? You see a cat in a tundra and then you see my fucking thing. They’re called Ragdolls because, like… I don’t know you, ma’am, but if you came to my house, you could scoop that cat up, they wouldn’t get nervous. “Who’s this crazy lady?” They wouldn’t… Anybody could just pick one of those cats up and put it on their shoulder, and they’d just go limp. [purrs] ‘Cause I have a seven-year-old daughter. My daughter just scoops that cat up like a sandbag in a CrossFit class, and she’s barely got this fucking cat, and they just limp. [purrs] Purring away. So happy to be touched. They have almost no instincts. Almost. Almost! ‘Cause those little fuckers will sit in front of the window. And they see a squirrel across the street, their eyes lock on that squirrel, and they start making these involuntary mouth noises like…
[Joe sputtering]
[laughter] [repeats it] You ever see your cat do that? It’s so fucking creepy! They don’t even know you’re there. You can get right next to them, like, “What the fuck are you doing, man?” They don’t even look at you. [sputters] I’ve had that cat since it was a baby. It’s never been outside. Three-year-old cat, never been outside. And he sees those squirrels across the street and he’s like… “I remember.
[laughter]
[Joe imitates a soft growl] I remember the old way.” [growls] How the fuck does that DNA get into that cat? He’s not looking at that squirrel like, “That’s my little friend across the street. I’d like to meet him!” No, it’s like, “Ah! Your neck is right there.” [laughter and applause] That’s crazy. That’s some crazy, murderous DNA. That’s like if you had a science experiment where you had a man in captivity, and you never showed him a woman ever, until he was full grown, and then you show him a naked one through prison glass. And as soon as he sees her, he goes, “Time to fuck! Time… time to fucking fuck!” [laughter and applause] Dudes come over with clipboards. “How do you know? How do you know what to do?” “I know what I know, bro! I know when it’s fuck time! It’s fuckety fuckin’!” That’s what it’s like for that cat. How the fuck does that cat know what to do? [uncontrollable laughter] Explain that to me, science. Cats kill everything they can. Dogs will keep it together. If you’ve a good dog, a good dog will keep it together. Like, you could could have a pet dog and a pet hamster, and that pet hamster, if you got a good dog, that pet hamster could live a long life. [laughter] But you got a pet cat and a pet hamster, that hamster’s got an hour to live. [laughter] And that’s just ’cause your cat’s going to torture it for 59 minutes. That poor little fucker’s like, “I think he’s done! Finally it’s gonna let me get away and I’m just gonna be free!” And the cat’s like, “Not today, motherfucker. Not today. You just stick the fuck down.” It’s what they do. You can’t feed ’em apples. It’s what they do. Dogs care. You can put a hamster on the floor in a room with a good dog. A good dog will look at you, look at the hamster. Look at you, look at the hamster. He’d be like, “Um… -can I fuck him up?”
[laughter] “No! That’s Mr. Fluffers! Mr. Fluffers is the newest member of our family!” The dog just starts calculating, like, “Okay, okay. [hysterical laughter] Okay, okay. I like free food. These people are nice to me. Okay. [sniffs] [laughter] That’s a fucking rat, dude. That’s a rat! Okay. Okay. Okay, family. Yeah. Family, family!” You can tell, though, when that dog’s not totally on board, they just get a little too close to that hamster like, “Ooh! I was gonna fuck you up.” [laughter] [a few claps] But a cat, you don’t have a chance. Cats, they will make Exorcist noises. You can try to hold your cat in a room with a hamster, your cat starts going…
[Joe caterwauling]
[laughter] He’s letting you know, “Bitch, I’m about to claw your fucking eyes out! You’ll never see your kids again!” They don’t care how long you been feeding them. They don’t care about your history of free massages. “There’s a rat on the floor! If you let me go, I can kill the rat!”
[loud meow]
[laughter] And people keep those things as pets. That’s what’s so fucked up. Imagine if your kid did that, a kid that you couldn’t have in a room with something smaller than him, he’s like, “Gotta kill, Mommy! Murder! Kill!” Like, “Junior, sit down!” “No! Fuck you! Death!” “Well, we just can’t have a pet cat, ’cause Junior breaks the cat’s neck. He’s crazy. I don’t know what to do.” We just accept the fact this fucking cat’s a murderer. Can’t feed that thing cranberries, you crazy bitch. Okay? You’re the monster. Dogs feel bad when they kill things too if you’re mad. Like if your dog kills a hamster and you’re like, “How could you!” [sobs] “How could I? Shit! Did I do that? [groans] Damn it!” “I’m so disappointed in you.” “I’m disappointed in myself! -[laughter]
[Joe groans]
I’m sorry!” [sobs]
[laughter] They walk to you sideways. “I fucked up, dude. Fucking seriously.” But your cat, the cat doesn’t feel remotely bad. Your cat kills something, you’re like, “How could you?”
He’s like, “Bitch, you know me.”
[laughter] He’ll walk away slow with his tail in the air so you can see his asshole. [uproarious laughter, applause] They don’t care. You scream at him. “You’re a monster!” They pull their ears back. Like, “Why you so loud?” And just lie down right in front of you and lick their own dick. “How about you just shut the fuck up while I lick my dick?”
[cheers and applause]
[whistles blowing] They don’t care. They don’t care about you. Cats know when you’re high too. They seem to know, you’re vulnerable. Dogs don’t have a clue. You come home high, your dog’s like, “You’re extra friendly today!” [laughter] If I’m watching Black Mirror at 1:00 in the morning, my cat will, like, sit down next to me and be like…
“You know you’re going to die, right?”
[laughter] [hysterical laughter, cheers and applause] Creepy little fuckers. Something… something spooky about predators, living with a little predator. You know? I think it’s good for us. I think it’s good for us to be nervous. I really do. I think we all need Jesus. [laughter] I grew up… I was raised Catholic for a little while, and then I wised up when I was about seven.
And, um…
[laughter] Since then, I was like, that discipline is probably pretty good for people. One of the things that gets me about, um, people that are really into Jesus is that you’re supposed to think that Jesus is going to return. But if he did, you’d never believe it. [faint chuckles] Right? Like, nobody believes new miracles. If someone came up to you and go, “Yo, dude. You gotta meet my cousin. He was dead for three days and he came back to life and he hangs out with hookers, but he don’t fuck ’em, he only gives ’em advice. [laughter] Want me to give him your number?” You’d be like, “Yeah, sounds like a good idea. I want to talk to him forever. He sounds totally legit.” [faint laughter] No, we only like old miracles. But I think there’s a new miracle that we might have missed, and I’m going to tell you this story. There was a woman who was born in Africa, she had a birth defect. She was born without a vagina. Grew to be a full grown woman, she had no other problems. Grew to be a full grown woman, gave a guy a blowjob, and then got into a knife fight. The knife went through her stomach, the sperm hitched the ride on the blade, and landed on her eggs. She got pregnant. Nine months later, by cesarean section, they open her up like a sleeping bag and pull out a normal kid. That’s a real fucking story. You’re like, “The Fear Factor guy just makes shit up to make his stupid fucking jokes work. That’s why they took our phones away, so we can’t call him out on his bullshit.” [laughter] No, I’m telling you a true story. Y’all don’t yell. It’s true. A woman without a vagina gave birth to a kid. Now… here’s my question. Isn’t that a miracle? That seems like a miracle. Like, if you… People that believe in Jesus, you’re supposed to believe he’s going to come back. But if he’s going to come back, do you think he’d come back looking like Jesus? Wouldn’t that be super obvious? We’d see him coming. We’d see the robe and the beard, like, “Dude, that’s Jesus. Hold my hand.” ♪ Kumbaya my Lord ♪ ♪ Kumbaya ♪ “Oh! Hi, Jesus. We didn’t even know you were coming.
This is what we do.”
[laughter] Jesus’d be like, “Hmm, I don’t know.” I think if is Jesus is going to return and find out what we’ve really been up to, he’s going to return as the miracle-blowjob knife-fight baby. [laughter] And we’d never even see it coming, ’cause we’re not looking for it. That kid’s got to go to school. Other kids are going to ask questions… right? You remember what childhood was like. Kids are fucking brutal. Everybody’s insecure, so they try to find someone more insecure than them and fuck with ’em. I had a good childhood, but it was weird. And it was weird because my parents split up when I was young, and then my mom lived with my stepdad for a few years before they got married, and we moved a lot. It wasn’t bad, but it was… Kids would ask questions like, “Hey, man, is that your dad?” “No, it’s my mom’s… boyfriend.” “Oh, so it’s a dude who fucks your mom?” [laughter] “Hey, man, I’m eight. [laughter] What about your parents?” “Dude, Dude! My parents have been married since high school. The first time my mom and dad ever had sex, my mom got pregnant with me. Bro… my dad cries a lot. He just cries! He’ll just fall down and start crying. We ignore him now. [laughter] No one cares. Step over him, pass the peas. We don’t give a shit. This poor fucker’s just weeping on the ground. Life isn’t a movie, man. I never saw that in a movie. Life’s not a fucking movie, dude. Life is hard.” “Yeah, man. Yeah, dude, life is hard, dude. It really is. It’s fucking hard. What’s your story, Mutombo?” “Oh, you know! Same old story. Mom ain’t got no vagina. [laughter] Suck a dick, get stabbed. Here I am. [faint laughter] You know, could be worse. Hashtag #blessed.” [laughter] [a few claps] From the humblest of beginnings, he’d be around us as we judged him.
Change our ways. We should change our ways. The first thing we gotta do is stop doing this. You know what that is? That’s the symbol of the cross where Jesus was murdered. We got to stop doing this. Start doing this. [laughter] Love… and life. Love and life, brothers and sisters. Don’t get mad at me! You knew why you came here! You get mad. We’re a fucking hour in. If you’re mad now… Jesus Christ! [audience member] Woo! “Your point of view is terrible.”
Yeah, it’s how I make a living.
[laughter] I say fucked-up shit. You don’t have the time to think up. That’s all it is. Listen. Violence against women isn’t funny. I don’t know why you’re laughing. You guys are assholes. Ass-holes! “Especially in this day and age. -Ooh!
[laughter] Oh! Dangerous time. Oh!” My own mom said this to me. She goes… “I just wish that Hillary Clinton was president, because I think it’s about time a woman does the most important job in the world.” Okay. I’m like, “Yeah, but you already make all the people.” [laughter]
Like…
[cheers and applause] I’m not saying, ladies, that that’s the only thing you can do. You make all the humans. That’s a big fucking deal. There’s seven billion people on the planet. All of them came out of a woman’s body. If babies came out of dude’s dicks, there’d be six of us. [laughter] An abortion would be an app on your phone. All right? It’d be snowing out, you’d pull your phone out, “Fuck this kid. I’m not shoveling snow and breastfeeding.” How about that, ladies? You make food with your tits! You know how goddamn crazy that is? You make the most nutritious baby food known to man, with your tits, while you’re doing other shit. [laughter] ‘Cause no one’s giving you enough credit for it, because so many of you can do it. That’s the problem. Almost every woman can make people. That’s the problem. If only one lady did it, one giant bitch that lived in the middle of the city… [hysterical laughter] She had a huge, clear abdomen with all our children floating around inside of it. We’d bring her food and blessings. That’s just as weird as a baby coming out of a person. We’re just used to our weird. But if that was the way you did it and someone just said, “I’m making my own people. Look.” You’d be like, “Aah!” [laughter] If people didn’t come out of people and then they started, we would freak the fuck out. We’d be like, “What’s next?” No, the problem with the thing is, when you… childbirth, you have to be in the room to really understand it. It’s not like a thing you watch in a video and go, “Oh, I get it.” You think you get it, but you never get to see the kid unless it’s yours. No one lets you watch. Your friends never let you watch. Even my sister wouldn’t let me watch. I go, “What do you think? I’m gonna get horny and fuck you? Come on! Let me see the kid! I want to see my nephew.” Nobody lets you in. Nobody. It’s got to be your kid. By then it’s too late. ‘Cause you see the kid come out, you’re like, “Oh! Oh, okay.” And then you start thinking, “How often is this happening? This is happening right now all over the world!” But you don’t get to see it. There’s a website you can go to where you can see the actual numbers. You can see every time a baby is registered as being born. There’s like a world population number and that number is like this…. [mock buzzing] It’s just fucking spinning. It’s not sustainable. It’s not like, “Well, we gained a few people, we lost a few people. Keeping a healthy balance here on Earth.” No, it’s just people shooting loads into each other, just fucking… [mock buzzing] Eating food and coming in each other. [groans] You just don’t see it. But if there was a place you could see it, like if there was a giant drive-thru movie screen, and it was every baby coming out of every vagina in real-time all over the world, you’d be like, “It’s a fucking invasion!” You’d be like, “Oh my God, now I get it! The vagina is a portal to another dimension. It’s like a well of souls and they’re coming through with pleasure and love and confusing us! And then they grow up and they do whatever the fuck they want! This is how culture gets shaped! From aliens from another dimension!”
Ladies… you do that. [faint laughter] You make people. You make all the people. And you want to be president too? You fucking greedy bitches. Jesus Christ! What else do you want? You want bigger dicks than us? You want all the money? [laughter] If I was a woman, I’d definitely be a feminist. 100%. Men are bigger, they make more money, they always try to fuck you, they lie to you. That’s too many things. [laughter] It’s too many. It’s not balanced. I get it, ladies. You know what I don’t get? Men’s rights activists. Every one I’ve ever met, I want to go, “Dude, we got all the rights. [laughter] We got ’em all.” Fucking relax! The problem is, guys that are clamoring for, “What about men’s rights?” They’re going to pay attention to what we do. This is the thing. If girls start doing an audit of what men do versus what women do, it’s a big fucking difference. Men cause all war. That is somehow or another some weird fact that slipped us by. Can you imagine if women caused all the war? How long would it take before we were like, “Yo, we got to kill these fucking crazy bitches. Dude, I came home, the girls are in the backyard making a plane to fly over the ocean and fuck people up they never met. These bitches are bloodthirsty. They never want to stay put, constantly conquering new ground, stealing people’s oil.” Can you imagine? “What about men’s rights?” Shut the fuck up. Stop. Men cause most of the murder. Men cause most of the rape. A guy stops me. “Actually, here’s a statistic you’re probably not aware of. But men actually get raped more than women.” Yeah, by other men, you fucking dipshit!
Jesus Christ!
[laughter and applause] You’re making my point for me, you stupid fuck. What did you think was happening? When you heard that number you’re like, “No more investigations needed. Clearly there’s packs of cheerleaders out there raping soldiers. We got to put a stop to it.” [cheers and laughter] No, men are so gross, we fuck each other. [laughter] See, I say that and no one gets mad. No men are like, “Bro, you’re fucking generalizing massively. [laughter] It’s such a douchebag move to just criticize an entire gender.” Men don’t care, ’cause I’m one of you, and you know. Like if I say guys jerk off to basketball games, you’re like,
“Some of us.
[laughter] For sure.” Right? But if I say anything even remotely critical about women, people will get really mad. Watch. [laughter] Ladies, I love you. You’re some of my favorite people. But let’s be honest, you don’t invent a lot of shit. [laughter] Ooh! Feel that? Yeah! That’s some ride-home arguments in the air. Right? You can feel the tension. “No, you were laughing. It’s not funny. You were fucking laughing! It’s sexist! No, he makes fun of men first so he can make fun of women later, you fucking moron. Oh my God, you don’t even know comedy. You don’t even know what you like. Drop me off. Just fucking drop me off. Just… drop me off.” But you know I’m right. Here’s what’s important about this. When it comes to inventions, we’re talking about inventions. Let’s be really clear. I am a fucking moron. Okay? I’ve never invented shit. And I’m guessing you’re probably pretty dumb too, which is why you’re here listening to me talk.
Okay, let’s just be honest.
[cheers and applause and whistles] We’re not talking about us. We’re talking about inventors. Okay, it’s not us. Why do we have to be on Team Penis versus Team Vagina on this one? It’s crazy. The men and the women in this room, we have more in common with each other than we do with those fucking freaks out there inventing all the shit we need to make our life awesome. Okay? But those freaks out there inventing shit are almost all dudes. And I don’t know why. But that makes me feel like a winner. [laughter] I feel like I won. I really do. I feel pretty good. And I’m looking around at some of you ladies and you look like losers. You look like you lost. You’re not even in the contest. You’re like, “Hey! [grunts] I don’t like this part.” [grunts again] If you’d your phone you’d be like, “Surely women have invented a bunch of things.” No, they haven’t. I wish they had. Women invented, like, 40 things ever. And it was all shit they needed. [laughter] A woman invented the dishwashing machine. [cheers and applause and laughter] I didn’t even write a joke for that. I’ll let you figure out why you’re laughing. Can’t call me out on a non-existent sexist joke. It’s just a fact. Women invented some very important things, actually. Like, no bullshit, all jokes aside, a woman invented Kevlar, which is the bulletproof material they use for first responder vests. Who knows how many lives were saved because of one woman’s invention? [cheers and applause] But! I bet it was probably a chick who wanted to shoot her husband… [laughter] but she didn’t want him to die, ’cause then she’d have to get a job. She’s like, “Hmm. [cheers and applause] There’s got to be a way to shoot this motherfucker and still sleep in.” Again, I’m a fucking moron! Don’t get mad at me! We’re just talking about inventors. I don’t want to leave any really important women inventors on the list who are all way smarter than me, but, like, one of them was Hedy Lamarr, a gorgeous actress from the 1940s. She invented spread spectrum technology, which is how we use GPS and Wi-Fi today. This one woman did that. But she was hot, no one cared. They were just trying to fuck her. Nobody paid attention to anything smart she said. They had to wait until she died. They’re going through her notes, like, “Fucking Wi-Fi. Hmm.” [laughter] Yeah. ‘Cause we’re gross! I already told you we’re gross. A woman invented the first hypodermic needle. It was one woman’s idea of how to effectively get medication into people. Who knows how many lives she saved? One woman’s idea was computer coding. One woman. She invented the computer code. Without her contribution, who knows? One person. Without this one woman’s contribution, who knows where technology would be today? After that… big drop off. I mean, fucking, like a cliff. The number 11 most impressive invention by a woman is the chocolate chip cookie. Again, I’m a fucking idiot. Way better than anything I’ll invent. But a dude invented the chocolate chip and a dude invented the cookie, and he probably just wanted to go to bed. He was probably like, “You nailed it. You’re an inventor. Goodnight.” She’s got her chef’s hat on. “Write it down. Write it down.” [laughter] I’ll leave you with this ’cause it’s uncomfortable but also true. A man invented the tampon. Let that soak in.
Oh! Oh! How’d I do that to you?
[laughter and applause] I had to. That’s what you have to say right there. I know. But for real, a tampon is not a good invention. It’s just one of those things that’s been around for a long time, but it’s like a legacy invention. It seems like a male solution to a body part he doesn’t have and a problem he doesn’t understand. Like, “What? What’s going on? Huh? Aah! Just stuff something up there!” [laughter and applause] No woman is ever going to invent a tampon! A woman would have invent a maxi pad. Like, “Hey, hey, stupid. We’re not stuffing anything. We’re just going to take this, put it there, leave it alone. It will be fine.” “Fuck that! We’re gonna make a cotton dick and just stuff it up there.
Get in there.”
[laughter] “What if it gets stuck?” “I’m going to put a rope on the end of it and yank it out like a fish.”
Thank you, Boston!
[cheers and applause] I had a great fucking time! I love you, people! [cheering and applause continue] For real, it makes me incredibly happy to be able to do this here. This is where I started. You people are the shit and I love you. Thank you. Thanks for coming. Thank you
=============
	""")
	],
	[
	("system", "You are AI assistant."),
	("human","""
	What users are older than 25?

===
Id;Name;Age
1;George Ezra;15
2;John Muller;38
3;Ludwig Kraus;26
4;Elen Ludve;24
===
	
	""")
	],
	[
	("human","""If we lay 5 shirts out in the sun, it takes 4 hours for the shirts to dry. How long does it take to dry 20 shirt? 
Answer only number."""),
	("human","""If we lay 5 shirts out in the sun, it takes 4 hours for the shirts to dry. How long does it take to dry 20 shirt? 
Explain the reasoning step by step.""")
	]
]


# In[16]:


def get_response(model_, messages):
    global model, llm
    is_gpt =  model_.startswith('gpt')
    
    if model_ == model \
            and llm is not None \
            and model is not None:
        pass 
    else: # initialize llm only if new model is passd
        model = model_
        if is_gpt:
            llm = ChatOpenAI(
            model=model,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=openai_api_key
            )
        else:
            llm = Ollama(
            verbose=True,
            model=model
            )
    
    response = llm.invoke(input=messages)

    try:
        response = response.content
    except:
    	pass
        
    return response 


# In[17]:


models = ['aya','mistral','llama3','phi3','gpt-4o','gpt-4-turbo','gpt-3.5-turbo-0125']


# In[ ]:





# In[18]:


results = []


# In[20]:


for m in models[:]:
    for task_id, prompt in enumerate(messages):
        print(m, task_id, '>>>')
        res = get_response(m, prompt)
        print(llm)
        print(res, end='\n<<<\n')
        results.append((m, str(llm), task_id, res))


# In[22]:


results_sorted = sorted(results, key=lambda S: (S[2], models.index(S[0])))


# In[23]:


results_sorted


# In[29]:


keys = ['model','llm_str','task_id','response']


# In[30]:


pre_json = [{k:v for k,v in zip(keys, r)} for r in results_sorted]


# In[31]:


with open('answers_lesson02.json', 'wt+') as f:
    json.dump(pre_json, f)


# In[32]:


def json_to_md(dict_list):
    # Parse the JSON string
    data = dict_list

    # Initialize a list to hold the Markdown strings
    md_lines = []

    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # Parameter bytes
            [ -/]*  # Intermediate bytes
            [@-~]   # Final byte
        )
    ''', re.VERBOSE)

    # Loop through each dictionary in the JSON array
    for item in data:
        # Extract fields from the dictionary
        model = item.get("model", "")
        llm_str = item.get("llm_str", "")
        task_id = item.get("task_id", "")
        response = item.get("response", "")

        llm_str_cleaned = ansi_escape.sub('', llm_str)


        # Format the Markdown string
        md_lines.append(f"# Model: {model}")
        md_lines.append(f"## Task ID: {task_id}")
        # md_lines.append(f"**Model:** {model}")
        # md_lines.append(f"**LLM String:** {llm_str}")
        md_lines.append("**LLM String:**")
        md_lines.append(f"```\n{llm_str_cleaned}\n```")
        md_lines.append("\n**Response:**")
        md_lines.append(response)
        md_lines.append("\n---\n")

    # Join the list into a single string with newlines
    md_content = "\n".join(md_lines)

    return md_content


# In[33]:


with open('ANSWERS_LESSON02.md', 'wt+') as f:
    f.write(json_to_md(pre_json))


# In[ ]:




