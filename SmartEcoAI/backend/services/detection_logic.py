from collections import Counter


class DetectionLogic:
    def summarize(self, detections):
        labels = [item.get("label", "unknown") for item in detections]
        counts = Counter(labels)
        return {
            "total": len(detections),
            "labels": dict(counts),
            "top_label": counts.most_common(1)[0][0] if counts else "none",
        }
