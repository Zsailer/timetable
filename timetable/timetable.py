from .handlers import ContainerHandler
from .day import Day

class TimeTable(ContainerHandler):
    """ Object that contains a Timetable to construct schedules. This object
    describes the days in week, periods in day, courses in period, and
    instructors in periods.

    This object is passed into a schedule object along with a student list
    object. The scheduler object will match students to a TimeTable object.

    Arguments
    ---------
    *Days : optional arguments

    Metadata
    --------
    timetable = {
        "Days" : [
            {
                "id" : "DAY000001",
                "name" : "Monday"
                "Periods" : [
                    "PER0000001",
                    "PER0000002",
                    "PER0000003",
                    ...
                ]
            },
            {
                "id" : "DAY000002",
                "name" : "Tuesday"
                "Periods" : [
                    "PER0000004",
                    "PER0000005",
                    "PER0000006",
                    ...
                ]
            }
        ],
        "Periods" : [
            {
                "id" : "PER0000001",
                "time" : "9AM",
                "Courses" : [
                    "COU000001",
                    "COU000002",
                    ...
                ]
            },
            {
                "id" : "PER0000002",
                "time" : "10AM",
                "Courses" : [
                    "COU000003",
                    "COU000004",
                    ...
                ]
            },
        ]
        "Courses" : [
            {
                "id" : "COU000001",
                "name" : "Math 7"
                "Instructor" : "INS000001",
            },
            {
                "id" : "COU000002",
                "name" : "Science 8"
                "Instructor" : "INS000002",
            }
        ],
        "Instructors" : [
            {
                "id" : "INS000001",
                "name" : "Bob",
            },
            {
                "id" : "INS000002",
                "name" : "Alice"
            }
        ]
    }
    """
    def __init__(self, *Days, **attrs):
        super(TimeTable, self).__init__(*Days, **attrs)
        self.keys = ["Days", "Courses", "Periods", "Instructors"]

    @property
    def days(self):
        """Get dictionary of Day objects. """
        return self._contents

    @property
    def metadata(self):
        """Get all metadata contained within a TimeTable object (pulling from
        all subobject within).
        """
        metadata = dict([(key,{}) for key in self.keys])
        for day in self.days:
            metadata["Days"].append(day.attrs)
            for period in day.period:
                metadata["Periods"].append(period.attrs)
                for course in period.courses:
                    metadata["Courses"].append(course.attrs)
                    for instructor in course.instructor:
                        metadata["Instructors"].append(instructor.attrs)
        return metadata

    @property
    def _child_type(self):
        return Day
