from django import template

register = template.Library()

@register.filter()
def youtube_embed(video_url):
    """
    Converts a YouTube URL into an embed URL.
    """
    embed_url = video_url.replace("watch?v=", "embed/")
    return f"{embed_url}?&amp;controls=0;&rel=0"