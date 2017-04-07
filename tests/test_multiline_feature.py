import os
import pyexcel


def test_reading_multiline_ods():
    testfile = os.path.join("tests", "fixtures", "multilineods.ods")
    sheet = pyexcel.get_sheet(file_name=testfile)
    assert sheet[0, 0] == '1\n2\n3\n4'
    assert sheet[1, 0] == 'Line 1\n\nLine 2'


def test_writing_multiline_ods():
    content = "2\n3\n4\n993939\n\na"
    testfile = "writemultiline.ods"
    array = [[content, "test"]]
    pyexcel.save_as(array=array, dest_file_name=testfile)
    sheet = pyexcel.get_sheet(file_name=testfile)
    assert sheet[0, 0] == content
    os.unlink(testfile)
