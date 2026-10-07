from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_sample_pdf(filename="sample_study_material.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor='#1A365D',
        spaceAfter=12
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor='#2B6CB0',
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        spaceAfter=8
    )

    story = []

    story.append(Paragraph("🎓 Computer Science Lecture Notes: AI & ML Fundamentals", title_style))
    story.append(Paragraph("<b>Course:</b> CS401 - Artificial Intelligence", body_style))
    story.append(Paragraph("<b>Topic:</b> Machine Learning Paradigms & Neural Networks", body_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Introduction to Artificial Intelligence", heading_style))
    story.append(Paragraph("Artificial Intelligence (AI) is an interdisciplinary field of computer science dedicated to creating systems capable of performing tasks that typically require human intelligence. These tasks include visual perception, speech recognition, decision-making, and language translation.", body_style))
    
    story.append(Paragraph("2. Machine Learning Paradigms", heading_style))
    story.append(Paragraph("Machine Learning (ML) is a core subfield of AI that enables systems to automatically learn and improve from experience without being explicitly programmed.", body_style))
    story.append(Paragraph("<b>Supervised Learning:</b> Models are trained on labeled datasets containing both input features and corresponding target output labels. Common algorithms include Linear Regression, Logistic Regression, Support Vector Machines (SVM), and Decision Trees.", body_style))
    story.append(Paragraph("<b>Unsupervised Learning:</b> Algorithms analyze unlabeled data to discover hidden patterns, underlying structures, or natural groupings. Common techniques include K-Means Clustering and Principal Component Analysis (PCA).", body_style))
    story.append(Paragraph("<b>Reinforcement Learning:</b> Agents learn optimal behaviors by interacting with a dynamic environment through trial and error, receiving rewards for positive actions and penalties for mistakes.", body_style))

    story.append(Paragraph("3. Neural Networks & Deep Learning", heading_style))
    story.append(Paragraph("Artificial Neural Networks (ANNs) are computational models inspired by the biological neural structures of the human brain. An ANN consists of interconnected nodes called neurons arranged in layers: an input layer, one or more hidden layers, and an output layer.", body_style))
    story.append(Paragraph("<b>Deep Learning:</b> Refers to training artificial neural networks with multiple hidden layers to extract high-level feature representations from raw input data.", body_style))
    story.append(Paragraph("<b>Overfitting:</b> Occurs when a model memorizes specific noise in the training dataset instead of learning general patterns, causing poor performance on unseen test data.", body_style))

    doc.build(story)
    print(f"Sample PDF successfully generated: {filename}")

if __name__ == "__main__":
    create_sample_pdf("c:\\Users\\purva\\OneDrive\\Desktop\\AI_STUDY_BUDDY\\sample_study_material.pdf")
