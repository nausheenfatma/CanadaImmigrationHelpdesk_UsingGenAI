This a project for learning and information purposes (not for commercial use):

Problem Statement: 

The Canada.ca website (https://www.canada.ca/en.html) is the official web portal of the Government of Canada. It's designed to provide centralized access to government information, programs, and services for the public, businesses, and visitors. Currently, due to the information coverage in the website, it is often daunting to search back and forth through several pages when searching for a very specific question in mind. Even though the website has a search tool bar, it return several pages while quering and the user has to go through all of them.

Proposed Solution and Goals:

I am building a Generative AI chat assistant (starting from immigration related enquiries usecase) to answer some of the user questions in a precise and user friendly manner without having to search through multiple pages.

Few Goals to start with (To be updated as the project progresses):

1. The assistant will have Agentic capabilities to use Routers to decide which of the following tools to choose:


    i. Question Answering Tool:  The chat assistant agent will be able to answer questions in a consise manner without the user having to scroll multiple pages back and forth of the Canada.ca website.

    Examples: 

        i) Question: Can I still apply using LMIA route?

        ii) Question: Can I drive in Canada after my immigration on my home country's driving license?

        iii) Question: Can I apply for my spouse's open work permit while he is already visiting Canada?


    ii. Calculator tool(s): 
        
    Few examples of how calculators can be invoked:
        
        i) Question: I have a family PR application: myself, my spouse and 2 kids. How much will be my total fees?

        ii) Question: I applied for immigration in January 2025. How long should my application take to process?


2. Build a simple Web Interface and host the chat assistant.