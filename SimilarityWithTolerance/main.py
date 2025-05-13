import re
from cdifflib import CSequenceMatcher # Using the C version for speed

# This function tokenizes text into words and also stores their character offsets
def get_words_with_offsets(text_input):
    words = []
    # Store (char_start_offset, char_end_offset) for each word
    char_offsets = []
    # Using \S+ to capture sequences of non-whitespace characters as words.
    # The .lower() is applied to the whole text once before this function if needed.
    for match in re.finditer(r'\S+', text_input):
        words.append(match.group(0)) # Store the word itself (could be omitted if only offsets needed for matcher)
        char_offsets.append((match.start(), match.end()))
    return words, char_offsets

def findSimilarPatterns_word_based(text1_orig, text2_orig, min_word_match_length=10, merge_gap_threshold=20):
    """
    Finds similar patterns between two texts using a word-based approach with CSequenceMatcher.

    Args:
        text1_orig (str): The first text.
        text2_orig (str): The second text.
        min_word_match_length (int): The minimum number of words for a match to be considered.
        merge_gap_threshold (int): The maximum character gap in text1 for merging adjacent matches.

    Returns:
        list: A list of tuples, where each tuple is (a_start, a_end, b_start, b_end)
              representing the character offsets of the merged similar patterns
              in text1_orig and text2_orig respectively.
    """
    # Lowercase texts once at the beginning
    text1_lower = text1_orig.lower()
    text2_lower = text2_orig.lower()

    words1, offsets1 = get_words_with_offsets(text1_lower)
    words2, offsets2 = get_words_with_offsets(text2_lower)

    # If either text has no words, no matches are possible.
    if not words1 or not words2:
        return []

    # Initialize CSequenceMatcher with lists of words
    matcher = CSequenceMatcher(None, words1, words2, autojunk=False)

    raw_matches_char_offsets = []
    for block in matcher.get_matching_blocks():
        # block.a: start index in words1
        # block.b: start index in words2
        # block.size: number of matching words
        if block.size == 0: # Skip the terminating sentinel block if present
            continue

        if block.size >= min_word_match_length:
            # Convert word indices back to character offsets using the stored offsets
            # Ensure indices are valid (get_matching_blocks should provide valid ones)
            orig_a_char_start = offsets1[block.a][0]
            # End offset is the end of the last word in the match
            orig_a_char_end = offsets1[block.a + block.size - 1][1]

            orig_b_char_start = offsets2[block.b][0]
            orig_b_char_end = offsets2[block.b + block.size - 1][1]
            
            # Optional: If you still need to filter by character length of the stripped match
            # (as in your original code with `len(text_to_display) > 20`), you could add it here:
            # matched_text_segment_a = text1_orig[orig_a_char_start:orig_a_char_end]
            # if len(matched_text_segment_a.strip()) <= 20: # Example character threshold
            #     continue

            raw_matches_char_offsets.append(
                (orig_a_char_start, orig_a_char_end, orig_b_char_start, orig_b_char_end)
            )

    if not raw_matches_char_offsets:
        return []

    # Sort matches by their start position in the first text (text1_orig) for merging.
    # The original code sorted by size first, then by position.
    # Sorting by start position is crucial for the merging logic.
    # get_matching_blocks already returns blocks typically ordered by their appearance in sequence a.
    # If they are not strictly sorted by a_start, this sort is essential.
    positions_sorted = sorted(raw_matches_char_offsets, key=lambda m: m[0])
    
    # Merging logic (adapted from your original code)
    merged_positions = []
    
    current_a_start = positions_sorted[0][0]
    current_a_end = positions_sorted[0][1]
    current_b_start = positions_sorted[0][2]
    current_b_end = positions_sorted[0][3]

    for i in range(1, len(positions_sorted)):
        next_a_start, next_a_end, next_b_start, next_b_end = positions_sorted[i]

        # Merge if the next match in text1 starts close to or before the end of the current merged block
        if (next_a_start - current_a_end) < merge_gap_threshold:
            # Extend the current merged block.
            # The end of the merged block becomes the end of the last constituent match.
            current_a_end = next_a_end
            current_b_end = next_b_end
        else:
            # Gap is too large, finalize the previous merged block
            merged_positions.append((current_a_start-(min_word_match_length+1), current_a_end-(min_word_match_length+1), current_b_start, current_b_end))
            # Start a new merged block
            current_a_start = next_a_start
            current_a_end = next_a_end
            current_b_start = next_b_start
            current_b_end = next_b_end

    # Append the last processed or merged block
    merged_positions.append((current_a_start, current_a_end, current_b_start, current_b_end))
    
    return merged_positions
