from django.db import models
class SourceType(models.TextChoices):
    WHATSAPP = "WHATSAPP", "WhatsApp"
    EMAIL = "EMAIL", "Email"
    INSTAGRAM = "INSTAGRAM", "Instagram"
    NOTES = "NOTES", "Notes"
    OTHER = "OTHER", "Other"

class ContentType(models.TextChoices):
    TEXT = "text", "Text"
    IMAGE = "image", "Image"
    VIDEO = "video", "Video"
    AUDIO = "audio", "Audio"
    DOCUMENT = "document", "Document"
    LINK = "link", "Link"
    OTHER = "other", "Other"