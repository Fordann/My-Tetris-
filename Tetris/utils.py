
def from_mask_to_string(mask):
    return int("".join(str(x) for x in mask), 2)
