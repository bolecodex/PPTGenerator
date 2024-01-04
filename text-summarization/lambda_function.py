import os
import json
from openai import OpenAI
def lambda_handler(event, context):
	
	client = OpenAI(
	    api_key=os.environ.get("OPENAI_API_KEY"),
	)
	
# 	text = "The New Year is the time or day at which a new calendar year begins and the calendar's year count increments by one. Many cultures celebrate the event in some manner.[1] In the Gregorian calendar, the most widely used calendar system today, New Year occurs on January 1 (New Year's Day, preceded by New Year's Eve). This was also the first day of the year in the original Julian calendar and the Roman calendar (after 153 BC).[2] Other cultures observe their traditional or religious New Year's Day according to their own customs, typically (though not invariably) because they use a lunar calendar or a lunisolar calendar. Chinese New Year, the Islamic New Year, Tamil New Year (Puthandu), and the Jewish New Year are among well-known examples. India, Nepal, and other countries also celebrate New Year on dates according to their own calendars that are movable in the Gregorian calendar. During the Middle Ages in Western Europe, while the Julian calendar was still in use, authorities moved New Year's Day, depending upon locale, to one of several other days, including March 1, March 25, Easter, September 1, and December 25. Since then, many national civil calendars in the Western World and beyond have changed to using one fixed date for New Year's Day, January 1—most doing so when they adopted the Gregorian calendar."
	text = event.get('text')
	
	messages =[
	# {"role":"system", "content": "You are a helpful assistant."},
	# {"role":"user", "content": f"Give me a summary about {text} within 200 charactors"}
    {"role": "system", "content": "Input Article: " + text},
    {"role": "system", "content": "User will ask you to shorten the Input Article. Make sure that the shortened version captures all the key points. \n  Response format: Keep the format of the Input Article. \n Output only the shortened article."},
    {"role": "user", "content": "Shorten the Input Article."}
	]

	chat_completion = client.chat.completions.create(
	    messages=messages,
	    model="gpt-3.5-turbo",
	)

	gpt_response = chat_completion.choices[0].message.content
	
	print("gpt_response:", gpt_response)
	return json.dumps(gpt_response)