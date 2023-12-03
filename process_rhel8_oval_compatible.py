from os import path

from bs4 import BeautifulSoup


def process_rhel8_oval_compatible():
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

    processed_file = f"{path.splitext(file_to_parse)[0]}_processed_oval_compatible.xml"
    with open(processed_file, "w", encoding="utf-8") as fd:
        fd.write(xml_tree.prettify())


if (__name__ == "__main__"):
    process_rhel8_oval_compatible()
