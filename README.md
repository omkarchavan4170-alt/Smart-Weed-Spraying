# Smart Weed Spraying — Software-Only Simulation

A software prototype for crop/weed detection, timing compensation, and virtual nozzle spraying. No hardware is required.

## Quick start
1. Install Python 3.10 or 3.11.
2. Create an environment and install packages:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Generate synthetic delay data:
   ```bash
   python -m src.generate_delay_data
   ```
4. Train the delay model:
   ```bash
   python -m src.train_delay_model
   ```
5. Run the software simulation (works without a trained weed detector):
   ```bash
   python -m simulation.run_simulation
   ```
6. Optional: train YOLO after placing a labeled YOLO-format dataset under `data/raw/`:
   ```bash
   yolo detect train data=data/data.yaml model=yolov8n.pt imgsz=640 epochs=50
   ```
   Copy the resulting `best.pt` to `models/weed_detector.pt` if you want image inference.

## Dataset notes
- The included simulation uses synthetic targets and does not need an image dataset.
- For image-based weed detection, see the dataset links supplied with this project in the chat.
- Keep class IDs consistent with `data/data.yaml`. If your dataset uses only weeds as a single class, edit `data.yaml` and `config.yaml` accordingly.
- Do not claim real-world latency or spray accuracy from synthetic simulation alone.

## Outputs
- `data/synthetic/scenarios.csv`
- `data/synthetic/delay_training.csv`
- `logs/timing_log.csv`
- `logs/spray_log.csv`
- `outputs/plots/`
