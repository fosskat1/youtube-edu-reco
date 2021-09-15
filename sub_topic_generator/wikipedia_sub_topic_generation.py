import wikipediaapi

KEY_PHRASES = ["concept", "application", "fundamentals", "principles"]


def fuzzy_match(raw_category):
    category = raw_category.lower()
    for phrase in KEY_PHRASES:
        if phrase in category:
            return True
    if category + " stub" in category:
        return True


# unused function to print categories that fuzzy match key_phrases
def print_category_members(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        # only print categories that are fuzzy matches (but keep searching)
        if fuzzy_match(c.title):
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_category_members(c.categorymembers, level=level + 1, max_level=max_level)


# unused function to print sections under a page
def ser(sections):
    for section in sections:
        print(section.title, "lists" in section.title.lower())
        if "lists" in section.title.lower():
            print(section)
        for sub_section in section.sections:
            ser(sub_section.sections)


def get_physics_sub_topics():
    wiki_wiki = wikipediaapi.Wikipedia('en')
    category = "List_of_physics_concepts_in_primary_and_secondary_education_curricula"
    cat = wiki_wiki.page(f"{category}")
    sub_topics = [f"Physics {section.title}" for section in cat.sections]
    print(sub_topics)


get_physics_sub_topics()






