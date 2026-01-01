def downsample_mean(rows: dict, factor: int) -> list:
    """
    Downsample a list of dict-like rows by averaging values over fixed-size chunks.
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
