from os import path

from bs4 import BeautifulSoup


def process_rhel8_oval_noncompatible():
    file_to_parse = "rhel-8.oval.xml"
    
    with open(file_to_parse, "r", encoding="utf-8") as fd:
        xml_tree = BeautifulSoup(fd, features="lxml-xml")

    # remove test "Red Hat Enterprise Linux must be installed" from all definitions
    for criteria_to_remove in xml_tree.find_all(test_ref="oval:com.redhat.rhba:tst:20191992005"):
        criteria_to_remove.decompose()

    # remove test "Red Hat Enterprise Linux must be installed" itself
    test_to_remove = xml_tree.find(id="oval:com.redhat.rhba:tst:20191992005")
    if (test_to_remove):
        test_to_remove.decompose()

    # remove related state
    state_to_remove = xml_tree.find(id="oval:com.redhat.rhba:ste:20191992005")
    if (state_to_remove):
        state_to_remove.decompose()

    # remove tests "Red Hat Enterprise Linux 8 is installed" and "Red Hat CoreOS 4 is installed"
    # from all definitions, but save it in variable
    for a_common_test in xml_tree.find_all(test_ref="oval:com.redhat.rhba:tst:20191992003"):
        common_criteria = a_common_test.parent.extract()

    # create a new tag "common_criteria" inside the "oval_definitions" tag
    common_criteria_tag = xml_tree.new_tag("common_criteria")
    # put there tests from the common_criteria variable
    common_criteria_tag.append(common_criteria)
    # put this tag in xml tree right before the "definitions" tag
    xml_tree.oval_definitions.definitions.insert_before(common_criteria_tag)

    processed_file = f"{path.splitext(file_to_parse)[0]}_processed_oval_noncompatible.xml"
    with open(processed_file, "w", encoding="utf-8") as fd:
        fd.write(xml_tree.prettify())


if (__name__ == "__main__"):
    process_rhel8_oval_noncompatible()
