from cdifflib import CSequenceMatcher

# positions = [(4419, 4468), (5347, 5409), (5413, 5563), (5565, 5595),(5999, 6095)]
def findSimilarPatterns(text,text2):
  matcher = CSequenceMatcher(None,text.lower(),text2.lower(),autojunk=False)
 # longest_match = matcher.find_longest_match()
 # text[longest_match.a:longest_match.a+longest_match.size]
  #text2[longest_match.b:longest_match.b+longest_match.size]

  positions = []
  for matched in sorted(matcher.get_matching_blocks(),key=lambda matched:matched.size,reverse=True):
    text_to_display = text[matched.a:matched.a+matched.size].strip()
    if len(text_to_display) > 20:
      positions.append((matched.a,
                        matched.a+matched.size,
                        matched.b,
                        matched.b+matched.size))


  positions.sort(key=lambda pair:pair[0])

  a_start = positions[0][0]
  a_end = positions[0][1]
  b_start = positions[0][2]
  b_end = positions[0][3]

  new_positions = []
  for i in range(len(positions)):
    difference_with_prev = positions[i][0] - a_end

    if difference_with_prev < 20:
      a_end = positions[i][1]
      b_end = positions[i][3]

    else:
      new_positions.append((a_start,a_end,b_start,b_end))
      a_start = positions[i][0]
      a_end = positions[i][1]
      b_start = positions[i][2]
      b_end = positions[i][3]

  new_positions.append((a_start,a_end,b_start,b_end))
  return new_positions
