from cdifflib import CSequenceMatcher

difflib.SequenceMatcher = CSequenceMatcher
matcher = CSequenceMatcher(None,text.lower(),text2.lower(),autojunk=False)
longest_match = matcher.find_longest_match()
text[longest_match.a:longest_match.a+longest_match.size]
text2[longest_match.b:longest_match.b+longest_match.size]

positions = []
for matched in sorted(matcher.get_matching_blocks(),key=lambda matched:matched.size,reverse=True):
  text_to_display = text[matched.a:matched.a+matched.size].strip()
  if len(text_to_display) > 20:
    #print(text_to_display)
    positions.append((matched.a,matched.a+matched.size))
    pass
