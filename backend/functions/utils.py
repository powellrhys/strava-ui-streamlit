# No depdendency imports needed for this file

def downsample_mean(rows, factor):
    """
    Downsample a list of dict-like rows by averaging values over fixed-size chunks.

    Args:
        rows (list[dict]): Sequence of rows with identical numeric keys.
        factor (int): Number of consecutive rows to average into one.

    Returns:
        list[dict]: Downsampled rows where each value is the mean over a chunk.
    """
    # Assume all rows share the same keys
    keys = rows[0].keys()
    result = []

    # Process rows in chunks of size `factor`
    for i in range(0, len(rows), factor):
        chunk = rows[i:i + factor]

        # Compute mean for each key within the chunk
        averaged = {
            k: sum(row[k] for row in chunk) / len(chunk)
            for k in keys
        }
        result.append(averaged)

    return result
