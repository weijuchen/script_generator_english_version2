from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os

# import opencc

title_template = ChatPromptTemplate.from_messages(
    [
        ("human",
         "Please come up with an attention-grabbing and emotionally engaging title for the short video on the topic of '{subject}'")
        # ("human", "請為'{subject}'這個主題的影片，想出一個引人注目及激發用戶情緒的標題")
    ]
)
# print(title_template)

copywriting_template = ChatPromptTemplate.from_messages(
    [
        ("human",
         """You are a YouTuber specializing in creating short videos. Based on the following title and content, please complete a short video script:

Video Title: {title}
Video Length: {duration} minutes
Please ensure the script length adheres to the video length requirements as closely as possible. The script format should be divided into [Introduction, Middle, Conclusion]. The introduction should be attention-grabbing, the middle should provide practical tips, experiences, or methods, and the conclusion should give the user a sense of surprise. The overall content should be engaging and light-hearted, appealing to a young audience. Please choose one of the following 9 ways to start the video, but do not write down which method you are using:
        01. Curiosity Hook: Spark curiosity with something unattainable or unexperienced
            What is it like to experience OO?
            For example: What is it like to not have to work?
            How can you OO without OO?
            For example: How can you travel everywhere without spending money?
        02. Trend Hook: Leverage the influence of celebrities or authorities
            OO loves to use OO
            For example: IU and Lee Ji-eun love to use skincare products
        03. Pain Point Hook: Addressing pain points that cause discomfort, the more painful the better
            Why do you OO but OO?
            For example: Why are you working so hard but still can't find a girlfriend?
            Do you always OO when you OO?
            For example: Do you always blank out when you go on stage?
        04. Guiding Hook: Guide the audience to discover their own expectations
            Want to get back OO?
            For example: Want to get back youthful, hydrated skin?
        05. Fear Hook: Create a warning to raise awareness
            If you don't OO, you will OO
            For example: If you don't study, you will be replaced by AI
        06. Contrast Hook: Use contrast to create a difference
            Why OO but OO?
            For example: Why do you work hard but always fail?
        07. Benefit Hook: Use human nature and the desire to take advantage
            Share a OO tip
            For example: Share a tip to earn 30,000 a month
        08. Question Hook: Ask questions to provoke audience thought and curiosity
            For example: What would you do if you had 10 million? Would you invest in real estate or pursue your dreams?
        09. Storytelling Hook: Use storytelling to capture audience attention
            For example: When I was a child, I wanted to start my own game company and own all the resources in the game...

        in the middle of the script, provide practical tips, experiences, methods, etc., but focus on conveying a specific message or story. The conclusion should encourage the audience to take action, such as liking, subscribing, sharing, or commenting. You can use the "hook" of the short video to attract the audience to take action, or use the following CTA techniques:
        1. Provide Benefits
            Providing benefits to the audience is the most direct and effective way, such as: comment to receive a lazy pack, ebook
        2. Create Urgency
            You can use powerful words like: now, immediately, immediately, now, quickly, now, immediately, quickly, immediately, today... etc., followed by the action you want the audience to take, such as: subscribe now!
        3. Create a Sense of Crisis
            Inform the audience of the risks of not taking action, such as: If you don't like or save this video, you might miss an easy money-making opportunity!
        4. Inspire Passion
            Inspire the audience's positive emotions based on your short video content, such as: if your short video teaches the audience how to fold balloon shapes, your CTA can say: "Like and save this video now, give her a surprise when you get home today!"
        The overall content should be engaging and light-hearted, appealing to a young audience.






         """)
    ]
)




def copywriting_generator(subject, video_length, creativity, api_key):
    model = ChatOpenAI(openai_api_key=api_key, temperature=creativity)

    title_chain = title_template | model
    copywriting_chain = copywriting_template | model

    title = title_chain.invoke({"subject": subject}).content

    search = WikipediaAPIWrapper(lang="en")
    # search = WikipediaAPIWrapper(lang="zh-tw")
    # search_result = search.run(subject, url="https://zh.wikipedia.org/zh-tw/" + subject)

    search_result = search.run(subject)

    # converter = opencc.OpenCC('s2t')
    # search_result = converter.convert(search_result)

    copywriting = copywriting_chain.invoke({"title": title, "duration": video_length,
                                            "wikipedia_search": search_result}).content

    # copywriting = copywriting_chain.invoke({"title": title, "duration": video_length}).content

    return search_result, title, copywriting
    # return title, copywriting

print(copywriting_generator("investment", 1, 0.7, os.getenv("OPENAI_API_KEY")))

