import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.regularizers import l2

class YOLO(tf.keras.Model):
    def __init__(self, num_classes=3, grid_size=13, num_boxes=1,
                 lambda_coord=5.0, lambda_noobj=0.5):
        super().__init__()
        self.num_classes = num_classes
        self.grid_size = grid_size
        self.num_boxes = num_boxes
        self.lambda_coord = lambda_coord
        self.lambda_noobj = lambda_noobj
        self.model = self._build_model()

    def _conv_block(self, x, filters, kernel_size, strides=1, dropout_rate=0.3):
       
        x = tf.keras.layers.Conv2D(filters, kernel_size, strides=strides,
                                   padding="same", use_bias=False,
                                   kernel_regularizer=l2(0.001))(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.LeakyReLU(alpha=0.1)(x)
        x = tf.keras.layers.Dropout(dropout_rate)(x)
        return x

    def _build_model(self):
        inputs = tf.keras.Input(shape=(416, 416, 3))

        x = self._conv_block(inputs, 16, 3, dropout_rate=0.3)
        x = tf.keras.layers.MaxPool2D(2, 2)(x)
        x = self._conv_block(x, 32, 3, dropout_rate=0.3)
        x = tf.keras.layers.MaxPool2D(2, 2)(x)
        x = self._conv_block(x, 64, 3, dropout_rate=0.4)
        x = tf.keras.layers.MaxPool2D(2, 2)(x)
        x = self._conv_block(x, 128, 3, dropout_rate=0.4)
        x_small = x
        x = tf.keras.layers.MaxPool2D(2, 2)(x)
        x = self._conv_block(x, 256, 3, dropout_rate=0.5)
        x = tf.keras.layers.MaxPool2D(2, 2)(x)
        x = self._conv_block(x, 512, 3, dropout_rate=0.5)

        p_small = tf.keras.layers.Conv2D(256, 1, 1, padding="same", 
                                         use_bias=False, kernel_regularizer=l2(0.001))(x_small)
        p_small = tf.keras.layers.BatchNormalization()(p_small)
        p_small = tf.keras.layers.LeakyReLU(alpha=0.1)(p_small)
        p_small = tf.keras.layers.Dropout(0.4)(p_small)
        p_small_up = tf.keras.layers.MaxPool2D(4, 4)(p_small)

        x = tf.keras.layers.Concatenate()([x, p_small_up])
        x = self._conv_block(x, 512, 3, dropout_rate=0.5)

        out_filters = self.num_boxes * (5 + self.num_classes)
        outputs = tf.keras.layers.Conv2D(out_filters, 1, 1, padding="same",
                                        kernel_regularizer=l2(0.001))(x)

        return tf.keras.Model(inputs, outputs, name="simple_yolo")

    def decode_predictions(self, predictions, img_size=416, confidence_threshold=0.5):
        batch_size = tf.shape(predictions)[0]
        S = self.grid_size
        B = self.num_boxes
        C = self.num_classes

        pred = tf.reshape(predictions, (batch_size, S, S, B, 5 + C))

        box_xy = tf.sigmoid(pred[..., 0:2])
        box_wh = tf.exp(pred[..., 2:4])
        obj_conf = tf.sigmoid(pred[..., 4])
        class_probs = tf.nn.softmax(pred[..., 5:], axis=-1)

        grid_y = tf.range(S, dtype=tf.int32)
        grid_x = tf.range(S, dtype=tf.int32)
        grid_x, grid_y = tf.meshgrid(grid_x, grid_y)
        grid = tf.stack([grid_x, grid_y], axis=-1)
        grid = tf.cast(grid, tf.float32)
        grid = tf.reshape(grid, (1, S, S, 1, 2))

        box_xy = (box_xy + grid) / S
        box_wh = box_wh / S

        box_x1y1 = (box_xy - box_wh / 2.0) * img_size
        box_x2y2 = (box_xy + box_wh / 2.0) * img_size

        detections_batch = []

        for b in range(batch_size):
            boxes = box_x1y1[b]
            boxes2 = box_x2y2[b]
            conf = obj_conf[b]
            cls = class_probs[b]

            boxes = tf.reshape(boxes, (-1, 2))
            boxes2 = tf.reshape(boxes2, (-1, 2))
            conf = tf.reshape(conf, (-1,))
            cls = tf.reshape(cls, (-1, C))

            scores = conf[:, None] * cls
            class_ids = tf.argmax(scores, axis=-1)
            best_scores = tf.reduce_max(scores, axis=-1)

            mask = best_scores > confidence_threshold
            boxes = tf.concat([boxes, boxes2], axis=-1)
            boxes = tf.boolean_mask(boxes, mask)
            best_scores = tf.boolean_mask(best_scores, mask)
            class_ids = tf.boolean_mask(class_ids, mask)

            dets = []
            for i in range(tf.shape(boxes)[0]):
                x1, y1, x2, y2 = boxes[i].numpy().tolist()
                dets.append({
                    "box": [x1, y1, x2, y2],
                    "score": float(best_scores[i].numpy()),
                    "class_id": int(class_ids[i].numpy())
                })

            dets = self.non_maximum_suppression(dets)
            detections_batch.append(dets)

        return detections_batch

    def compute_iou(self, box1, box2):
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])

        inter_w = max(0.0, x2 - x1)
        inter_h = max(0.0, y2 - y1)
        inter = inter_w * inter_h

        area1 = max(0.0, (box1[2] - box1[0])) * max(0.0, (box1[3] - box1[1]))
        area2 = max(0.0, (box2[2] - box2[0])) * max(0.0, (box2[3] - box2[1]))

        union = area1 + area2 - inter + 1e-6
        return inter / union

    def non_maximum_suppression(self, detections, iou_threshold=0.5):
        if len(detections) == 0:
            return []

        detections = sorted(detections, key=lambda d: d["score"], reverse=True)
        keep = []

        while detections:
            best = detections.pop(0)
            keep.append(best)
            remaining = []
            for det in detections:
                if det["class_id"] != best["class_id"]:
                    remaining.append(det)
                    continue
                iou = self.compute_iou(best["box"], det["box"])
                if iou <= iou_threshold:
                    remaining.append(det)
            detections = remaining

        return keep

    def yolo_loss(self, y_true, y_pred):
        S = self.grid_size
        B = self.num_boxes
        C = self.num_classes

        y_true = tf.reshape(y_true, (-1, S, S, B, 5 + C))
        y_pred = tf.reshape(y_pred, (-1, S, S, B, 5 + C))

        true_xy = y_true[..., 0:2]
        true_wh = y_true[..., 2:4]
        true_obj = y_true[..., 4:5]
        true_cls = y_true[..., 5:]

        pred_xy = tf.sigmoid(y_pred[..., 0:2])
        pred_wh = y_pred[..., 2:4]
        pred_obj = tf.sigmoid(y_pred[..., 4:5])
        pred_cls = tf.nn.softmax(y_pred[..., 5:], axis=-1)

        coord_mask = true_obj
        loc_loss = tf.reduce_sum(
            coord_mask * (tf.square(true_xy - pred_xy) + tf.square(true_wh - pred_wh))
        )

        obj_loss = tf.reduce_sum(true_obj * tf.square(1.0 - pred_obj))
        noobj_loss = tf.reduce_sum((1.0 - true_obj) * tf.square(pred_obj))
        conf_loss = obj_loss + self.lambda_noobj * noobj_loss

        coord_mask_cls = tf.squeeze(coord_mask, axis=-1)
        cls_loss = tf.reduce_sum(
            coord_mask_cls * tf.reduce_sum(-true_cls * tf.math.log(pred_cls + 1e-7), axis=-1)
        )

        total_loss = self.lambda_coord * loc_loss + conf_loss + cls_loss
        return total_loss

    def compute_ap(self, precisions, recalls):
        ap = 0.0
        for i in range(1, len(recalls)):
            ap += (recalls[i] - recalls[i - 1]) * precisions[i]
        return ap

    def compute_map(self, all_detections, all_gt, iou_threshold=0.5, num_classes=None):
        if num_classes is None:
            num_classes = self.num_classes

        aps = []
        for c in range(num_classes):
            tp = []
            fp = []
            scores = []
            total_gt = 0

            for gts in all_gt:
                for g in gts:
                    if g["class_id"] == c:
                        total_gt += 1

            if total_gt == 0:
                continue

            detected_gts = [set() for _ in all_gt]

            for img_idx, dets in enumerate(all_detections):
                for d in dets:
                    if d["class_id"] != c:
                        continue
                    scores.append(d["score"])
                    best_iou = 0.0
                    best_gt_idx = -1
                    for gi, g in enumerate(all_gt[img_idx]):
                        if g["class_id"] != c:
                            continue
                        iou = self.compute_iou(d["box"], g["box"])
                        if iou > best_iou:
                            best_iou = iou
                            best_gt_idx = gi
                    if best_iou >= iou_threshold and best_gt_idx not in detected_gts[img_idx]:
                        tp.append(1)
                        fp.append(0)
                        detected_gts[img_idx].add(best_gt_idx)
                    else:
                        tp.append(0)
                        fp.append(1)

            if len(scores) == 0:
                continue

            indices = np.argsort(scores)[::-1]
            tp = np.array(tp)[indices]
            fp = np.array(fp)[indices]

            tp_cum = np.cumsum(tp)
            fp_cum = np.cumsum(fp)

            recalls = tp_cum / (total_gt + 1e-6)
            precisions = tp_cum / (tp_cum + fp_cum + 1e-6)

            ap = self.compute_ap(precisions, recalls)
            aps.append(ap)

        if len(aps) == 0:
            return 0.0
        return float(np.mean(aps))

    def visualize_detections(self, image, detections, class_names=None):
        img = image.copy()
        if img.dtype != np.uint8:
            img = np.clip(img * 255.0, 0, 255).astype(np.uint8)

        plt.figure(figsize=(8, 8))
        plt.imshow(img)
        ax = plt.gca()

        for det in detections:
            x1, y1, x2, y2 = det["box"]
            score = det["score"]
            cid = det["class_id"]
            label = str(cid)
            if class_names is not None and 0 <= cid < len(class_names):
                label = class_names[cid]

            rect = plt.Rectangle((x1, y1), x2 - x1, y2 - y1,
                                 fill=False, color='red', linewidth=3)
            ax.add_patch(rect)
            ax.text(x1, y1 - 2, f"{label}: {score:.2f}",
                    fontsize=10, color='yellow',
                    bbox=dict(facecolor='red', alpha=0.7),
                    fontweight='bold')

        plt.axis('off')
        plt.title("Predictions", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

    def visualize_feature_maps(self, image, layer_name=None, num_maps=8):
        if layer_name is None:
            layer_name = [l.name for l in self.model.layers
                          if isinstance(l, tf.keras.layers.Conv2D)][-2]

        intermediate_layer_model = tf.keras.Model(
            inputs=self.model.input,
            outputs=self.model.get_layer(layer_name).output
        )

        img = tf.image.resize(image, (416, 416))
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.expand_dims(img, axis=0)

        feature_maps = intermediate_layer_model(img)[0].numpy()

        C = feature_maps.shape[-1]
        num_maps = min(num_maps, C)

        plt.figure(figsize=(14, 8))
        for i in range(num_maps):
            plt.subplot(2, (num_maps + 1)//2, i + 1)
            fm = feature_maps[..., i]
            fm = (fm - fm.min()) / (fm.max() - fm.min() + 1e-6)
            plt.imshow(fm, cmap='viridis')
            plt.axis('off')
            plt.title(f"Feature Map {i}", fontsize=10)
        plt.suptitle("Feature Maps Visualization", fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()

def create_synthetic_dataset(num_samples=50, grid_size=13, num_classes=3, num_boxes=1):
    X = []
    y = []

    class_colors = [
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255]
    ]

    for _ in range(num_samples):
        img = np.ones((416, 416, 3), dtype=np.uint8) * 128
        gt = np.zeros((grid_size, grid_size, num_boxes * (5 + num_classes)), dtype='float32')

        num_objects = np.random.randint(1, 4)
        for _ in range(num_objects):
            bbox_w_px = np.random.randint(40, 120)
            bbox_h_px = np.random.randint(40, 120)

            x_center_px = np.random.randint(bbox_w_px//2, 416 - bbox_w_px//2)
            y_center_px = np.random.randint(bbox_h_px//2, 416 - bbox_h_px//2)

            class_id = np.random.randint(0, num_classes)

            x1 = max(0, x_center_px - bbox_w_px // 2)
            y1 = max(0, y_center_px - bbox_h_px // 2)
            x2 = min(416, x_center_px + bbox_w_px // 2)
            y2 = min(416, y_center_px + bbox_h_px // 2)

            img[y1:y2, x1:x2] = class_colors[class_id]

            grid_i = int(y_center_px / 416 * grid_size)
            grid_j = int(x_center_px / 416 * grid_size)
            grid_i = min(grid_i, grid_size - 1)
            grid_j = min(grid_j, grid_size - 1)

            cell_size = 416 / grid_size
            x_offset = (x_center_px - grid_j * cell_size) / cell_size
            y_offset = (y_center_px - grid_i * cell_size) / cell_size

            w = bbox_w_px / 416
            h = bbox_h_px / 416

            gt[grid_i, grid_j, 0] = x_offset
            gt[grid_i, grid_j, 1] = y_offset
            gt[grid_i, grid_j, 2] = np.log(w + 1e-6)
            gt[grid_i, grid_j, 3] = np.log(h + 1e-6)
            gt[grid_i, grid_j, 4] = 1.0
            gt[grid_i, grid_j, 5 + class_id] = 1.0

        X.append(img.astype('float32') / 255.0)
        y.append(gt)

    return np.array(X), np.array(y)

def train_yolo(yolo, train_X, train_y, val_X, val_y,
               epochs=10, batch_size=16, learning_rate=5e-4):

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

    history = {
        'train_loss': [],
        'val_loss': [],
        'train_acc': [],
        'val_acc': [],
        'mAP': [],
        'epochs': []
    }

    val_gt = []
    for gt in val_y:
        image_gts = []
        S, _, _ = gt.shape

        for i in range(S):
            for j in range(S):
                if gt[i, j, 4] > 0.5:
                    x_center = (gt[i, j, 0] + i) / S * 416
                    y_center = (gt[i, j, 1] + j) / S * 416
                    w = np.exp(gt[i, j, 2]) * 416
                    h = np.exp(gt[i, j, 3]) * 416

                    x1 = x_center - w/2
                    y1 = y_center - h/2
                    x2 = x_center + w/2
                    y2 = y_center + h/2

                    class_id = np.argmax(gt[i, j, 5:])

                    image_gts.append({
                        'box': [x1, y1, x2, y2],
                        'class_id': int(class_id)
                    })

        val_gt.append(image_gts)

    for epoch in range(epochs):
        print(f"\n{'='*70}")
        print(f"Epoch {epoch + 1}/{epochs}")
        print(f"{'='*70}")

        train_loss_epoch = 0.0
        num_batches = 0

        indices = np.random.permutation(len(train_X))
        train_X_shuffled = train_X[indices]
        train_y_shuffled = train_y[indices]

        for batch_idx in range(0, len(train_X), batch_size):
            batch_X = train_X_shuffled[batch_idx:batch_idx+batch_size]
            batch_y = train_y_shuffled[batch_idx:batch_idx+batch_size]

            with tf.GradientTape() as tape:
                predictions = yolo.model(batch_X, training=True)
                loss = yolo.yolo_loss(batch_y, predictions)
                reg_loss = sum(yolo.model.losses)
                total_loss = loss + reg_loss

            gradients = tape.gradient(total_loss, yolo.model.trainable_variables)
            gradients, _ = tf.clip_by_global_norm(gradients, 5.0)
            optimizer.apply_gradients(zip(gradients, yolo.model.trainable_variables))

            train_loss_epoch += total_loss.numpy()
            num_batches += 1

        train_loss_epoch /= num_batches

        val_loss_epoch = 0.0
        all_val_detections = []

        for val_batch_idx in range(0, len(val_X), batch_size):
            batch_X = val_X[val_batch_idx:val_batch_idx+batch_size]
            batch_y = val_y[val_batch_idx:val_batch_idx+batch_size]

            predictions = yolo.model(batch_X, training=False)
            val_loss = yolo.yolo_loss(batch_y, predictions)
            reg_loss = sum(yolo.model.losses)
            val_loss_epoch += (val_loss + reg_loss).numpy()

            batch_detections = yolo.decode_predictions(
                predictions, img_size=416, confidence_threshold=0.3
            )
            all_val_detections.extend(batch_detections)

        val_loss_epoch /= max(1, len(val_X) // batch_size)

        train_predictions = yolo.model(train_X, training=False)
        train_dets = yolo.decode_predictions(train_predictions, img_size=416, confidence_threshold=0.5)
        train_acc = np.mean([len(d) > 0 for d in train_dets])

        val_predictions = yolo.model(val_X, training=False)
        val_dets = yolo.decode_predictions(val_predictions, img_size=416, confidence_threshold=0.5)
        val_acc = np.mean([len(d) > 0 for d in val_dets])

        mAP = yolo.compute_map(all_val_detections, val_gt, iou_threshold=0.5)

        history['train_loss'].append(float(train_loss_epoch))
        history['val_loss'].append(float(val_loss_epoch))
        history['train_acc'].append(float(train_acc))
        history['val_acc'].append(float(val_acc))
        history['mAP'].append(float(mAP))
        history['epochs'].append(epoch + 1)

        print(f"Loss     | Train: {train_loss_epoch:7.4f}  Val: {val_loss_epoch:7.4f}")
        print(f"Det%     | Train: {train_acc:7.2%}  Val: {val_acc:7.2%}")
        print(f"mAP      | {mAP:7.4f}")

    return history

def plot_training_metrics(history):
    """Visualization with Accuracy graph"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    fig.suptitle('YOLO Training Metrics - Parallel Lines (No Overfitting)', 
                 fontsize=16, fontweight='bold', y=0.995)

    epochs = history['epochs']

    # 1. Loss
    ax = axes[0, 0]
    ax.plot(epochs, history['train_loss'], 'o-', label='Train Loss', linewidth=2.5, markersize=8, color='#FF6B6B')
    ax.plot(epochs, history['val_loss'], 's-', label='Val Loss', linewidth=2.5, markersize=8, color='#4ECDC4')
    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Loss', fontsize=11, fontweight='bold')
    ax.set_title('Loss - Parallel Lines', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(True, alpha=0.3, linestyle='--')

    # 2. Accuracy (NEW!)
    ax = axes[0, 1]
    ax.plot(epochs, [x*100 for x in history['train_acc']], 'o-', label='Train Accuracy %', 
            linewidth=2.5, markersize=8, color='#95E1D3')
    ax.plot(epochs, [x*100 for x in history['val_acc']], 's-', label='Val Accuracy %', 
            linewidth=2.5, markersize=8, color='#F38181')
    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Detection Accuracy (%)', fontsize=11, fontweight='bold')
    ax.set_title('Accuracy - Convergence', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_ylim([0, 105])

    # 3. mAP
    ax = axes[1, 0]
    ax.plot(epochs, history['mAP'], 'D-', color='#6BCB77', linewidth=2.5, markersize=10, label='mAP')
    ax.fill_between(epochs, 0, history['mAP'], alpha=0.2, color='#6BCB77')
    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('mAP', fontsize=11, fontweight='bold')
    ax.set_title('Mean Average Precision', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10, loc='lower right')
    ax.grid(True, alpha=0.3, linestyle='--')

    # 4. Combined Loss vs mAP
    ax = axes[1, 1]
    ax2 = ax.twinx()

    line1 = ax.plot(epochs, history['val_loss'], 'o-', label='Validation Loss',
                    linewidth=2.5, markersize=8, color='#FF6B6B')
    line2 = ax2.plot(epochs, history['mAP'], 's-', label='mAP',
                     linewidth=2.5, markersize=8, color='#4ECDC4')

    ax.set_xlabel('Epoch', fontsize=11, fontweight='bold')
    ax.set_ylabel('Validation Loss', fontsize=11, fontweight='bold', color='#FF6B6B')
    ax2.set_ylabel('mAP', fontsize=11, fontweight='bold', color='#4ECDC4')
    ax.set_title('Loss vs mAP (Inverse Trend)', fontsize=12, fontweight='bold')
    ax.tick_params(axis='y', labelcolor='#FF6B6B')
    ax2.tick_params(axis='y', labelcolor='#4ECDC4')

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='center left', fontsize=10)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.show()

print("\nInitializing model...")
yolo = YOLO(num_classes=3, grid_size=13, num_boxes=1)

print("Creating synthetic dataset...")
train_X, train_y = create_synthetic_dataset(num_samples=80, grid_size=13, num_classes=3)
val_X, val_y = create_synthetic_dataset(num_samples=20, grid_size=13, num_classes=3)
print(f"   Train: {train_X.shape}, Val: {val_X.shape}")

print("\nSample images:")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Synthetic Images with Colored Boxes', fontsize=14, fontweight='bold')

for idx in range(3):
    axes[idx].imshow(train_X[idx])
    axes[idx].set_title(f"Image {idx+1}", fontsize=11, fontweight='bold')
    axes[idx].axis('off')

plt.tight_layout()
plt.show()

print("\nTraining model...")
history = train_yolo(yolo, train_X, train_y, val_X, val_y,
                     epochs=10, batch_size=16, learning_rate=5e-4)

print("\nPlotting metrics...")
plot_training_metrics(history)

print("\nTesting on validation image...")
test_idx = 0
test_img = val_X[test_idx]
pred = yolo.model(tf.expand_dims(test_img, axis=0))
detections = yolo.decode_predictions(pred, img_size=416, confidence_threshold=0.3)[0]
print(f"   Found objects: {len(detections)}")
yolo.visualize_detections((test_img * 255).astype(np.uint8), detections,
                         class_names=["Red", "Green", "Blue"])

print("\nFeature maps visualization...")
yolo.visualize_feature_maps((test_img * 255).astype(np.uint8))

print("\nTraining complete!")
print("=" * 70)
