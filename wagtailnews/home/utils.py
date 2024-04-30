
def get_top_tags():
    from home.models import Content
    all_tags = []
    all_contents = Content.objects.live().all()
    for content in all_contents:
        tags = content.tags.all()
        for tag in tags:
            if tag.name not in all_tags:
                all_tags.append(tag.name)
    max_number_of_tags = 6     
    return all_tags[:max_number_of_tags]

def get_all_hub_peek_articles():
    from home.models import Content
    all_tags = []
    all_hub_peeks = {}
    max_articles_in_hub_peek = 4
    
    tags = get_top_tags()
    for tag in tags:
        if tag not in all_tags:
            all_tags.append(tag)
            articles = Content.objects.filter(tags__name=tag).live().order_by('-first_published_at')
            all_hub_peeks[tag] = articles[:max_articles_in_hub_peek]
    return all_hub_peeks


def get_hub_peek_articles(tag):
    from home.models import Content
    all_hub_peeks = {}
    max_articles_in_hub_peek = 4
    articles = Content.objects.filter(tags__name=tag).live().order_by('-first_published_at')
    all_hub_peeks[tag] = articles[:max_articles_in_hub_peek]
    return all_hub_peeks