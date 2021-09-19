import wikipediaapi

KEY_PHRASES = ["concept", "application", "fundamentals", "principles"]


def fuzzy_match(search_string):
    """
    Determine if raw_category contains any of the words in list KEY_PHRASES
    :param search_string: str to search and determin if contains KEY_PHRASES
    :return: bool True if match, False if no match
    """
    search_string = search_string.lower()
    for phrase in KEY_PHRASES:
        if phrase in search_string:
            return True
    return False


# TODO: work on this fuction
def print_category_members(categorymembers, level=0, max_level=1):
    for c in categorymembers.values():
        # only print categories that are fuzzy matches (but keep searching)
        if fuzzy_match(c.title):
            print("%s: %s (ns: %d)" % ("*" * (level + 1), c.title, c.ns))
        if c.ns == wikipediaapi.Namespace.CATEGORY and level < max_level:
            print_category_members(c.categorymembers, level=level + 1, max_level=max_level)


def traverse_sections(sections, level=0, max_level=3):
    """
    Traverse page sections, print section titles
    :param sections: List of sections on a wiki_wiki.page()
    :return: None
    """
    for section in sections:
        print("%s %s %s" % (" " * (level), "*" * (level + 1), section.title))
        if level < max_level:
            traverse_sections(section.sections, level + 1)


def get_sections_from_topic(topic):
    """
    Given a topic return list of sections on page
    :return: List of section titles
    """
    wiki_wiki = wikipediaapi.Wikipedia('en')
    cat = wiki_wiki.page(f"{topic}")
    sub_topics = [{section.title} for section in cat.sections]
    return sub_topics


# POC for physics, with HARD CODED category
category = "List_of_physics_concepts_in_primary_and_secondary_education_curricula"
sections = get_sections_from_topic(category)
for section in [f"Physics {section.pop()}" for section in sections]:
    print(section)

# Search sections for topics
# wiki_wiki = wikipediaapi.Wikipedia('en')
# cat = wiki_wiki.page(f"Physics")
# traverse_sections(cat.sections)

# Test fuzzy match
# print(fuzzy_match("absconcepts"))







