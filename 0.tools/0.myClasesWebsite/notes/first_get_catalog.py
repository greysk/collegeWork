import json
from pathlib import Path
import re


def getcatalogpg(file: str | Path) -> list[dict]:
    """
    Obtain course details form a course catalog page in json file.

    This script was written to parse a json file that was created
    from a course catalog pdf using PyMuPDF.
        (https://pymupdf.readthedocs.io/en/latest/index.html)

    Args:
        file (str | Path): The course catalog page in json format.

    Returns:
        list[dict]: Each dict contains the following course details:
            catalog_code, title, credits, prereqs, description.
    """
    # Define regex pattern for finding catalog code.
    p_catalog_code = re.compile(r'(\w?\w\w)(\d\d\d\w?)')
    skip1 = ''.join(['* ENROLLMENT IN ALL NURSING (NURXXX) COURSES IS',
                     ' RESTRICTED TO STUDENTS ADMITTED TO A NURSING',
                     ' PROGRAM.'])
    skip2 = ''.join(['NURSING COURSES MUST BE TAKEN IN THE PRESCRIBED',
                     ' SEQUENCE NOTED IN THE DEGREE PROGRAM', ' CHART.'])

    # Load json course catalog page into memory.
    with open(file, 'r') as f:
        page = json.loads(f.read().strip())

    # Variable to hold each course's data.
    course: list = []
    # Variable to hold data of all courses in page.
    catalog_page: list = []
    # Go through json file to get text.  Start at index 2, because
    # first two blocks on page contains the page headers and footers.
    for block in page['blocks'][2:]:
        for line in block['lines']:
            for span in line['spans']:
                # Obtain the text.  Text order is the course catalog code,
                # title, number of credits, prerequisites, and multiple
                # `span['text']`s containing the course description.
                text = span['text']
                # Obtain stripped text to check for and skip warning text that
                # only shows on pages with Nursing courses.
                stripped_text = text.strip()
                skip_text = (stripped_text == skip1, stripped_text == skip2)
                # Start checking if we reached new course.  Don't start until
                # after course length is greater that 5, because description
                # starts at 5th item.  The course description is likely longer
                # than one `span['text']`, start checking immediately after
                # first description span to be safe.
                if len(course) > 5:
                    # Use regex code defined above to check for catalog code.
                    catalog_code = p_catalog_code.match(text)
                    if catalog_code or any(skip_text):
                        # Clean up completed course details, merging course
                        # description into a on string instead of a list
                        # containing multiple strings.
                        course_description = {
                            'code': course[0].strip(),
                            'title': course[1].strip(),
                            'credits': course[2].strip(),
                            'prereq': course[3][15:].replace(
                                'AND', '&').replace('OR', "|"),
                            'description': ''.join(course[4:])
                        }
                        # Save course_description to catalog_page.
                        catalog_page.append(course_description)
                        # Empty course list to start collecting the
                        # details of the next course on the page.
                        course.clear()
                if any(skip_text):
                    continue
                # Continue to collect or start collecting a course's details.
                course.append(text)
    return catalog_page
