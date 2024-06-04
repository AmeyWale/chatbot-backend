from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

chatbot = ChatBot("clgbot")

data = [
  # Questions about academics
  ["What are the average class sizes for my major?", "The average class size for [MAJOR] courses varies depending on the level (introductory vs. upper-level). However, it generally falls between [SIZE_RANGE]."],
  ["Does the college offer academic support services like tutoring or writing centers?", "Yes, the college offers a variety of academic support services. We have a [NAME_OF_TUTORING_CENTER] that provides tutoring for most subjects. There's also a [NAME_OF_WRITING_CENTER] to help students with their writing assignments."],
  # Questions about campus life
  ["What is the housing situation like on campus? Are there options for freshmen?", "We offer a variety of on-campus housing options, including residence halls, apartments, and suites. Freshmen are guaranteed on-campus housing for their first year."],
  ["What kind of student activities and clubs are there on campus?", "The college has a vibrant student life with over [NUMBER] clubs and organizations covering a wide range of interests. You can find clubs for [LIST_A_FEW_EXAMPLES]. There's also a student activities office that can help you find a club that fits your interests."],
  # Questions about finances
  ["What kind of financial aid does the college offer?", "The college offers a variety of financial aid options, including scholarships, grants, and work-study programs. We encourage you to visit our financial aid website ([FINANCIAL_AID_WEBSITE]) for more information."],
  # Open ended question
  ["Is there anything else you can tell me about the college experience at [COLLEGE_NAME]?", "We recommend checking out our website for more information about student life, academics, and campus resources. You can also attend a virtual or in-person campus tour to get a better feel for the college."]
]


trainer = ListTrainer(chatbot)
for training_data in data:
    trainer.train(training_data)


app = FastAPI()
origins = [
   "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/ask")
async def ask_bot(request:Request):

    data = await request.json()
 
    message = data.get("message")
    bot_response = chatbot.get_response(message)
    
    
    return {"response":str(bot_response)}

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=8000,reload=True)


