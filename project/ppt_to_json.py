from pptx import Presentation
import json

def ppt_to_json(ppt_file):
    prs = Presentation(ppt_file)
    slides_data = []

    for slide_number, slide in enumerate(prs.slides, start=1):
        # Initialize the slide data dictionary
        slide_data = {"slide_number": float(slide_number), "title": "", "content": "", "narration": ""}

        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            
            if shape == slide.shapes.title:
                slide_data["title"] = shape.text
            else:
                slide_data["content"] += shape.text + "\n"

        slides_data.append(slide_data)

    return slides_data

# Example usage
ppt_file = 'Marie_Curie_Presentation.pptx'
slides_json = ppt_to_json(ppt_file)
# print(slides_json)
print(json.dumps(slides_json, indent=4))
