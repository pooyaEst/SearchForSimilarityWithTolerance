exposes one function called `findSimilarPatterns(text1,text2)` which takes two strings and return an array of similarities the array is made of tuples of 4 inputs `(text1.start,text1.end,text2.start,text2.end)` text.start and text.end are positions in the string that are similar between two string inputs. while these are positions of similar texts text1[text1.start:text2.end] are not gonna be same as text2[text2.start:text2.end]as algorithm is tolerant of differences between two texts upto a point(20 characters for now) the reason for this tolerance is because of difference in getting the subtitles and transcripts like using AI or handwritten subtitles.
