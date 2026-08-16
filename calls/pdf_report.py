from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def create_pdf(call, response):

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    heading = styles["Heading2"]

    body = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            "AI Call Analysis Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"<b>Call:</b> {call.file_name}",
            body
        )
    )

    story.append(
        Paragraph(
            f"<b>Date:</b> {call.created_at.strftime('%d-%m-%Y %H:%M')}",
            body
        )
    )

    story.append(Spacer(1, 20))

    sections = [
        (
            "Overall Summary",
            call.summary
        ),
        (
            "Customer Issue",
            call.customer_issue
        ),
        (
            "Resolution",
            call.resolution
        ),
        (
            "Customer Sentiment",
            call.sentiment
        ),
        (
            "Agent Performance",
            call.agent_performance
        ),
        (
            "Key Topics",
            call.key_topics
        ),
        (
            "Action Items",
            call.action_items
        ),
    ]

    for heading_text, content in sections:

        story.append(
            Paragraph(
                heading_text,
                heading
            )
        )

        story.append(
            Paragraph(
                content or "Not available",
                body
            )
        )

        story.append(
            Spacer(1, 12)
        )

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    doc.build(story)