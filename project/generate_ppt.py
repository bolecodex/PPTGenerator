from pptx import Presentation
from pptx.util import Inches, Pt

# Create a presentation object
prs = Presentation()

# Updated slide data
slides_data = [
    {
        "slide_number": 1.0,
        "title": "Introduction to Albert Einstein",
        "content": "Albert Einstein was born on March 14, 1879 in Ulm, in the Kingdom of Württemberg in the German Empire. He is best known for developing the theory of relativity, which revolutionized the understanding of space, time, and gravity.",
        "narration": ""
    },
    {
        "slide_number": 2.0,
        "title": "Einstein's Contributions to Science",
        "content": "• E=mc^2: The mass-energy equivalence.\n• Theory of General relativity: This led to prediction of the deflection of light by gravity, concept of black holes and Big Bang theory.\n• Quantum Theory: Einstein made important contributions to early quantum theory.",
        "narration": ""
    },
    {
        "slide_number": 3.0,
        "title": "Einstein's Legacy",
        "content": "Einstein's work continues to influence the course of science to this day. His theories have been instrumental in developing GPS technology and understanding the universe. He was awarded the Nobel Prize in Physics in 1921.",
        "narration": ""
    }
]

# Function to add a slide
def add_slide(title, content):
    slide_layout = prs.slide_layouts[1]  # Using layout 1 for title and content
    slide = prs.slides.add_slide(slide_layout)
    title_placeholder = slide.shapes.title
    body_placeholder = slide.placeholders[1]

    title_placeholder.text = title
    tf = body_placeholder.text_frame
    tf.text = content

    for paragraph in tf.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(18)

# Add slides
for slide in slides_data:
    add_slide(slide['title'], slide['content'])

# Save the presentation
prs.save('Marie_Curie_Presentation.pptx')
