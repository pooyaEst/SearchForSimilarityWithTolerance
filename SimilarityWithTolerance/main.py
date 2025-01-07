def get_matching_blocks_fast(a: str, b: str, min_size: int = 20):
    """
    Find matching blocks between two strings, ignoring matches smaller than min_size.
    Returns list of tuples (i, j, size) where:
        - i is the start index in string a
        - j is the start index in string b
        - size is the length of the match
    
    Much faster than difflib for long strings when only interested in substantial matches.
    """
    # Create dictionary of all possible substring positions in b
    substrings = {}
    for i in range(len(b) - min_size + 1):
        substr = b[i:i + min_size]
        if substr not in substrings:
            substrings[substr] = []
        substrings[substr].append(i)
    
    # Find matches
    matches = []
    i = 0
    while i < len(a) - min_size + 1:
        substr = a[i:i + min_size]
        if substr in substrings:
            # Found a potential match, try to extend it
            for j in substrings[substr]:
                # Extend match forward
                size = min_size
                while (i + size < len(a) and 
                       j + size < len(b) and 
                       a[i + size] == b[j + size]):
                    size += 1
                
                # Only keep matches that meet minimum size
                if size >= min_size:
                    matches.append((i, j, size))
                    # Skip ahead by the match length to avoid overlapping matches
                    i += size - 1
                    break
        i += 1
    
    # Sort matches by position in first string
    matches.sort()
    
    # Remove contained matches
    filtered_matches = []
    last_end = 0
    for match in matches:
        if match[0] >= last_end:
            filtered_matches.append(match)
            last_end = match[0] + match[2]
    
    return filtered_matches

def findSimilarPatterns(text,text2):
  positions = []
  for matched in sorted(get_matching_blocks_fast(text,text2),key=lambda matched:matched[0],reverse=True):
    text_to_display = text[matched[0]:matched[0]+matched[2]].strip()
    if len(text_to_display) > 20:
      positions.append((matched[0],
                        matched[0]+matched[2],
                        matched[1],
                        matched[1]+matched[2]))


  positions.sort(key=lambda pair:pair[0])

  if len(positions)==0:
    return []

  a_start = positions[0][0]
  a_end = positions[0][1]
  b_start = positions[0][2]
  b_end = positions[0][3]

  new_positions = []
  for i in range(len(positions)):
    difference_with_prev = positions[i][0] - a_end

    if difference_with_prev < 10:
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
