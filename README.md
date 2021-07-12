# attendance_generator_website

### Rita Sharma (PCE teacher) told the students to make attendance. Got super annoyed and made this to help every teacher automatically generate attendance from the CSVs made by MS teams.
### Hosted at => (https://vedant-attendance-gen.glitch.me/)[website]

## Usage:
1) Select the CSV file for the first input
2) Select a text file containing names of the students in the second box.
3) Select a text file that includes the information about the starting hour of the lecture, ending hour of the lecture and the amount of time students are allowed outside the meeting, it should look like this:
  ```
  13:00
  15:00
  10
  ```
  Here 13:00 (or 1 PM) is the starting hour, 15:00 (or 3 PM) is the ending hour, and students will be marked absent if the total time inside the meeting is less that 1 hr, 50 mins.
 
