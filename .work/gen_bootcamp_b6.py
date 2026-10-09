"""Bootcamp video Phase 2, Batch B6: 12 bootcamps x 3 videos = 36 videos.
30s, 1280x720 @ 24fps, silent h264+aac-silent, burned-in captions,
"Preview -- narration coming" tag, .vtt + .narration.md staged alongside.
Styles: story / fireship / bbg / 3b1b / primer. Original animations only.
Modeled on gen_bootcamp_b5.py (do not modify the earlier batch files).

Filenames are bc- prefixed so they never collide with course videos.

Batch B6 bootcamps (Cloud Certifications):
  aws-clf, aws-data, aws-dop, aws-ml, aws-saa, aws-scs, aws-soa, az-104, az-305, az-700, azure-developer, oracle-oci
"""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_batch1 as G
from gen_batch1 import (
    font, lerp, clamp, ease, wrap_text, txt, dot_grid, glow_box,
    panel, arrow, caption_bar, preview_tag, title_card, end_card,
    bbg_title, code_panel, write_vtt, write_narration, encode_video,
    STYLE_BG, ACCENTS,
    TEAL, YELLOW, CYAN, MAGENTA, ORANGE, BLUE, GREEN, RED, GOLD, CREAM, WHITE, DIM,
    F_SANS, F_BOLD, F_MONO, F_MONOB, F_SERIF, F_SERIFB,
)

W, H, FPS, DUR, NFR = G.W, G.H, G.FPS, G.DUR, G.NFR
OUT = "/home/hatch/workspace/apex-audit/docs/assets/videos"
SMOKE = os.environ.get("SMOKE") == "1"

def bar(dr, x, y, w, h, frac, fill, label=None, val=None):
    dr.rectangle([x, y, x + w, y + h], fill=(18, 24, 40), outline=DIM, width=2)
    fw = int(w * clamp(frac))
    if fw > 4:
        dr.rectangle([x + 2, y + 2, x + fw - 2, y + h - 2], fill=fill)
    if label:
        txt(dr, (x, y - 8), label, font(F_SANS, 22), DIM, anchor="lb")
    if val:
        txt(dr, (x + w, y + h + 8), val, font(F_MONOB, 24), fill, anchor="rt")

# ============================================================
# aws-clf (bbg x2 + 3b1b x1)
def scene_aws_clf_shared(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Shared Responsibility: Who Patches What', CYAN)
    _boxes = ('AWS: of the cloud', 'facilities', 'hardware', 'network', 'hypervisor')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), "the model is the exam's favorite trick question", font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'AWS: of the cloud — you: in the cloud', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_clf_pricing(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Pay-As-You-Go: Three Ways to Pay', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'on-demand vs reserved vs spot', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('on-demand', 1.0, '$1.00/hr', RED), ('reserved 1-yr', 0.6, '$0.60/hr', YELLOW), ('spot', 0.3, '$0.30/hr', GREEN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'reserved for steady, spot for flexible, on-demand for spikes', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'the wrong model is a 70% tax on your architecture', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_clf_global(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Regions and AZs: The Global Map', CYAN)
    _nodes = [('us-e-1', 300, 300), ('AZ-a', 520, 220), ('AZ-b', 520, 380), ('eu-w-1', 900, 300), ('AZ-a', 1080, 220)]
    _edges = [(0, 1), (0, 2), (3, 4)]
    _order = (0, 1, 2, 3, 4)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'distance is latency — redundancy is survival', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'pick the region near your users, the AZs for your uptime', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-data (bbg x2 + fireship x1)
def scene_aws_data_pipeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Data Pipeline: S3 to Insight', CYAN)
    _boxes = ('kinesis', 'S3 lake', 'glue ETL', 'redshift', 'quicksight')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'stream, land, transform, warehouse, visualize', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'every stage scales independently — that is the whole trick', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_data_zones(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Lake Zones: Raw to Curated', CYAN)
    _layers = ('curated: analytics-ready', 'cleansed: schemas fixed', 'raw: land everything')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'raw is a swamp — curated is a product', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'never let analysts drink from the raw zone', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_data_stream(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'Streaming ETL in 100 Seconds', MAGENTA)
    _lns = [("for batch in kinesis.window('1m'):", (200, 200, 255)), ("    agg = batch.group_by('sku')", YELLOW), ("             .count('orders')", YELLOW), ("    agg.write.s3('s3://lake/curated/')", (200, 200, 255)), ('# window → aggregate → sink', GREEN), ('# exactly-once via checkpointing', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'stream_etl.py', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'windows turn infinity into batches', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'event time, not processing time — or your metrics lie', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-dop (bbg x1 + fireship x1 + primer x1)
def scene_aws_dop_pipeline(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'The Delivery Pipeline', CYAN)
    _boxes = ('codecommit', 'codebuild', 'codedeploy', 'cloudwatch')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'every commit rides the same conveyor', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'manual deploys are how outages are born', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_dop_bluegreen(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Blue/Green: The Zero-Downtime Swap', CYAN)
    _lp = ('serves 100% of traffic', 'old build, proven stable')
    _rp = ('new build deployed', 'smoke tests passing', 'zero live traffic')
    _nL = int(clamp((t - 5) / 6) * len(_lp))
    _nR = int(clamp((t - 12) / 6) * len(_rp))
    dr.rectangle([120, 190, 600, 470], fill=(16, 16, 30), outline=GREEN, width=3)
    txt(dr, (360, 232), 'BLUE (live)', font(F_BOLD, 26), GREEN, anchor="mm")
    for _i in range(_nL):
        txt(dr, (160, 290 + _i * 46), "\u2713 " + _lp[_i], font(F_SANS, 22), GREEN, anchor="lm")
    dr.rectangle([680, 190, 1160, 470], fill=(16, 16, 30), outline=RED, width=3)
    txt(dr, (920, 232), 'GREEN (new)', font(F_BOLD, 26), RED, anchor="mm")
    for _i in range(_nR):
        txt(dr, (720, 290 + _i * 46), "\u2717 " + _rp[_i], font(F_SANS, 22), RED, anchor="lm")
    if t > 20:
        dr.rectangle([300, 520, 980, 592], fill=(12, 24, 12), outline=GOLD, width=3)
        txt(dr, (W // 2, 556), 'flip the router — green is live, blue is the rollback', font(F_BOLD, 25), GOLD, anchor="mm")
def scene_aws_dop_cfn(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'CloudFormation in 100 Seconds', MAGENTA)
    _lns = [('Parameters:', YELLOW), ('  Env: {Type: String}', (200, 200, 255)), ('Resources:', YELLOW), ('  Web: {Type: AWS::EC2::Instance}', (200, 200, 255)), ('Outputs:', YELLOW), ('  URL: {Value: !GetAtt Web.PublicDns}', (200, 200, 255)), ('# declare it — then create the change set', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'stack.yaml', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'clickops is not a strategy — templates are', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'review the change set like a code diff', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-ml (bbg x1 + 3b1b x1 + primer x1)
def scene_aws_ml_sagemaker(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'SageMaker: Train, Tune, Deploy', CYAN)
    _boxes = ('train', 'tune', 'registry', 'endpoint', 'monitor')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'train, tune, deploy — then monitor', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'the model that ships is the one you can reproduce', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_ml_bias(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Bias Metrics: Count What Matters', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'fairness is a measurement problem', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'P(approve) by group · FPR gap · calibration error', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('approval gap', 18, '%d%%'), ('FPR gap', 11, '%d%%'), ('drift alerts', 7, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'if you cannot measure it, you cannot fix it', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'fairness is a metric before it is a value', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_ml_gradient(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Gradient Descent: Walking Downhill', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'the learning rate is the stride', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'w := w - η · ∇L(w)', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('training steps', 10000, '%d'), ('loss drop', 94, '%d%%'), ('epochs', 50, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'the learning rate is the stride length', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'overshoot the valley and you diverge', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-saa (bbg x2 + 3b1b x1)
def scene_aws_saa_arch(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Three-Tier Architecture', CYAN)
    _boxes = ('route53', 'ALB', 'EC2 ASG', 'RDS multi-AZ')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'stateless in front, stateful behind', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'scale each tier independently — that is the point', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_saa_failover(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Multi-AZ Failover: Surviving the Fire', CYAN)
    _nodes = [('primary', 320, 320), ('standby', 640, 320), ('app', 480, 520)]
    _edges = [(0, 1), (0, 2), (1, 2)]
    _order = (0, 1, 2)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'the standby is already warm — that is the whole design', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'synchronous replication is why RPO is near zero', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_saa_s3tiers(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'S3 Storage Classes: Pay for Access', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'hot data, cold price', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('standard', 1.0, '$23/TB', RED), ('intel-tier', 0.55, '$12.5/TB', YELLOW), ('glacier', 0.17, '$4/TB', GREEN), ('deep archive', 0.04, '$1/TB', TEAL)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'hot data, cold price — match the class to the pattern', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'lifecycle rules do the moving — set them on day one', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-scs (bbg x1 + fireship x1 + primer x1)
def scene_aws_scs_iam(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'IAM Policy Evaluation: The Gauntlet', CYAN)
    _layers = ('request context', 'SCP guardrails', 'identity policy', 'resource policy', 'explicit deny check')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'explicit deny always wins — memorize the order', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the exam hides the deny in the SCP', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_scs_kms(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Envelope Encryption: Keys Protect Keys', CYAN)
    _pts = [(200, 330), (460, 330), (720, 330), (980, 330)]
    _labels = ('KMS master', 'data key', 'encrypt object', 'store both')
    _m = len(_pts)
    _prog = clamp((t - 5) / 15)
    _pos = _prog * (_m - 1)
    _i = int(_pos)
    if _i >= _m - 1:
        _i = _m - 2
        _fr = 1.0
    else:
        _fr = _pos - _i
    for _k in range(_m - 1):
        _done = _pos > _k
        dr.line([_pts[_k][0], _pts[_k][1], _pts[_k + 1][0], _pts[_k + 1][1]],
                fill=CYAN if _done else DIM, width=4)
    for _k in range(_m):
        _px, _py = _pts[_k]
        _on = _pos >= _k - 0.001
        dr.ellipse([_px - 26, _py - 26, _px + 26, _py + 26],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_px, _py), str(_k + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_px, _py + 52), _labels[_k], font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    _tx = lerp(_pts[_i][0], _pts[_i + 1][0], _fr)
    _ty = lerp(_pts[_i][1], _pts[_i + 1][1], _fr)
    dr.ellipse([_tx - 13, _ty - 13, _tx + 13, _ty + 13], fill=YELLOW, outline=WHITE, width=2)
    if t > 19:
        txt(dr, (W // 2, 540), 'the data key never travels far', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'rotate the master — re-encrypt only the envelopes', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_scs_guardduty(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'GuardDuty Findings in 100 Seconds', MAGENTA)
    _lns = [('{', (200, 200, 255)), ('  "severity": 8,', RED), ('  "type": "Trojan:EC2/BlackholeTraffic",', YELLOW), ('  "resource": {"instanceId": "i-0abc"}', (200, 200, 255)), ('}', (200, 200, 255)), ('# severity 8+ → act now', GREEN), ('# read fields before paging humans', DIM)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'finding.json', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'read the finding, not the panic', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'severity is a number — treat it like one', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# aws-soa (bbg x1 + primer x1 + story x1)
def scene_aws_soa_scaling(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Auto Scaling: Breathe With Demand', CYAN)
    _items = [('02:00 load', 0.25, '2 inst', TEAL), ('09:00 spike', 1.0, '8 inst', RED), ('12:00 settle', 0.6, '5 inst', YELLOW), ('18:00 ease', 0.35, '3 inst', GREEN)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'scale out fast, scale in slow', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'cooldowns prevent the flap tax', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_soa_alarms(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'CloudWatch Alarms: Eyes Everywhere', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'alarm on symptoms, not causes', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'alarms evaluate every 60s', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('metrics tracked', 240, '%d'), ('alarms firing', 3, '%d'), ('auto-remediated', 41, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'alarm on symptoms, not causes', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'an alarm nobody actions is just noise', font(F_SANS, 24), DIM, anchor="mm")
def scene_aws_soa_backup(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["story"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'The 3 AM Restore', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'backups are tested restores', font(F_SERIF, 24), DIM, anchor="mm")
    _ev = [('detect: corruption pages at 3 AM', 5), ('locate: last good snapshot — 02:00', 9), ('restore to sandbox — never prod first', 13), ('verify the data — checksums match', 17), ('cut over — RTO met, go back to sleep', 21)]
    _n = len(_ev)
    _x = 500
    _top = (H - (_n - 1) * 76) // 2 + 44
    dr.line([_x, _top - 20, _x, _top + (_n - 1) * 76 + 20], fill=DIM, width=4)
    for _i, (_lb, _ts) in enumerate(_ev):
        _y = _top + _i * 76
        _done = t > _ts
        dr.ellipse([_x - 14, _y - 14, _x + 14, _y + 14],
                   fill=GOLD if _done else (40, 40, 60), outline=GOLD, width=2)
        txt(dr, (_x + 36, _y), _lb, font(F_SANS, 24), CREAM if _done else DIM, anchor="lm")
        if _done:
            txt(dr, (_x - 36, _y), "t+%ds" % int(_ts), font(F_MONO, 19), GOLD, anchor="rm")
    if t > 19:
        txt(dr, (W // 2, 624), 'backups are tested restores — nothing else', font(F_SERIF, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 668), 'rehearse the restore quarterly or it will fail yearly', font(F_SERIF, 24), DIM, anchor="mm")
# ============================================================
# az-104 (bbg x2 + fireship x1)
def scene_az104_rbac(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'RBAC Scopes: Who Can Touch What', CYAN)
    _layers = ('resource', 'resource group', 'subscription', 'management group')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'scope narrow — grant least privilege', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'deny beats allow, every single time', font(F_SANS, 24), DIM, anchor="mm")
def scene_az104_vnet(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'VNet Peering: The Private Highway', CYAN)
    _nodes = [('vnet-a', 280, 320), ('vnet-b', 640, 320), ('on-prem', 1000, 320)]
    _edges = [(0, 1), (0, 2)]
    _order = (0, 1, 2)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'private, fast, and off the public internet', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), "non-transitive peering is the exam's trap", font(F_SANS, 24), DIM, anchor="mm")
def scene_az104_arm(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'ARM Templates in 100 Seconds', MAGENTA)
    _lns = [('{', (200, 200, 255)), ('  "$schema": "arm#",', DIM), ('  "resources": [{', YELLOW), ('    "type": "Microsoft.Storage/storageAccounts",', (200, 200, 255)), ('    "sku": {"name": "Standard_LRS"}', (200, 200, 255)), ('  }]', YELLOW), ('}', (200, 200, 255)), ('# idempotent — what-if before deploy', GREEN)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'azuredeploy.json', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'declare the end state — never script the steps', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'what-if is the plan before the apply', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# az-305 (bbg x2 + 3b1b x1)
def scene_az305_landing(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Landing Zones: The Enterprise Foundation', CYAN)
    _boxes = ('hierarchy', 'policy', 'hub network', 'identity', 'operations')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'foundations are load-bearing — get them right once', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'refactoring a landing zone is agony — design it first', font(F_SANS, 24), DIM, anchor="mm")
def scene_az305_paired(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Paired Regions: Surviving the Outage', CYAN)
    _nodes = [('eastus', 280, 320), ('westus', 640, 320), ('traffic mgr', 1000, 320)]
    _edges = [(0, 2), (1, 2)]
    _order = (0, 1, 2)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), '300 miles apart for a reason', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'update domains are geography now', font(F_SANS, 24), DIM, anchor="mm")
def scene_az305_cost(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['3b1b'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), "Cost Optimization: The Architect's Levers", font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'every design decision has a price tag', font(F_SANS, 24), DIM, anchor="mm")
    _items = [('rightsizing', 0.9, '-35%', GREEN), ('reservations', 0.7, '-40%', TEAL), ('autoscale', 0.5, '-25%', YELLOW), ('orphan cleanup', 0.3, '-12%', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'every design decision has a price tag', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'a design without a cost model is a wish', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# az-700 (bbg x1 + fireship x1 + primer x1)
def scene_az700_dns(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'DNS Resolution: The 100ms That Matters', CYAN)
    _pts = [(180, 330), (440, 330), (700, 330), (960, 330)]
    _labels = ('stub query', 'recursive walk', 'authoritative', 'cached answer')
    _m = len(_pts)
    _prog = clamp((t - 5) / 15)
    _pos = _prog * (_m - 1)
    _i = int(_pos)
    if _i >= _m - 1:
        _i = _m - 2
        _fr = 1.0
    else:
        _fr = _pos - _i
    for _k in range(_m - 1):
        _done = _pos > _k
        dr.line([_pts[_k][0], _pts[_k][1], _pts[_k + 1][0], _pts[_k + 1][1]],
                fill=CYAN if _done else DIM, width=4)
    for _k in range(_m):
        _px, _py = _pts[_k]
        _on = _pos >= _k - 0.001
        dr.ellipse([_px - 26, _py - 26, _px + 26, _py + 26],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_px, _py), str(_k + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_px, _py + 52), _labels[_k], font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    _tx = lerp(_pts[_i][0], _pts[_i + 1][0], _fr)
    _ty = lerp(_pts[_i][1], _pts[_i + 1][1], _fr)
    dr.ellipse([_tx - 13, _ty - 13, _tx + 13, _ty + 13], fill=YELLOW, outline=WHITE, width=2)
    if t > 19:
        txt(dr, (W // 2, 540), 'every click starts with a lookup', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'TTL is a promise about staleness — keep it short when migrating', font(F_SANS, 24), DIM, anchor="mm")
def scene_az700_vwan(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Virtual WAN: Hub-and-Spoke at Scale', CYAN)
    _nodes = [('hub', 640, 300), ('spoke-a', 280, 480), ('spoke-b', 640, 520), ('spoke-c', 1000, 480)]
    _edges = [(0, 1), (0, 2), (0, 3)]
    _order = (0, 1, 2, 3)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'one hub, fifty spokes, zero mesh headaches', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'the hub is the only place routing gets interesting', font(F_SANS, 24), DIM, anchor="mm")
def scene_az700_nsg(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["fireship"])
    dot_grid(dr)
    bbg_title(dr, 'NSG Rules in 100 Seconds', MAGENTA)
    _lns = [('{', (200, 200, 255)), ('  "priority": 100, "port": 443,', GREEN), ('  "access": "Allow", "direction": "Inbound"', GREEN), ('  "priority": 4096,', DIM), ('  "access": "Deny"  // default, untouchable', RED), ('}', (200, 200, 255)), ('# first match wins — order is policy', YELLOW)]
    _hi = int(clamp((t - 5) / 13) * len(_lns))
    code_panel(dr, 190, 150, W - 190, 580, 'nsg-rules.json', _lns, hi_line=_hi, t=t)
    if t > 19:
        txt(dr, (W // 2, 622), 'lowest number wins — first match decides', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 662), 'log the denies and the typo confesses', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# azure-developer (bbg x1 + 3b1b x1 + primer x1)
def scene_azdev_functions(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Serverless Triggers: Code That Waits', CYAN)
    _boxes = ('http', 'queue', 'timer', 'blob', 'service bus')
    _n = len(_boxes)
    _w = 210 if _n <= 5 else 150
    _gap = 30 if _n <= 5 else 18
    _x0 = (W - (_n * _w + (_n - 1) * _gap)) // 2
    _lit = int(clamp((t - 5) / 13) * _n)
    _y0, _y1 = 270, 410
    for _i, _b in enumerate(_boxes):
        _x = _x0 + _i * (_w + _gap)
        _on = _i < _lit
        glow_box(dr, [_x, _y0, _x + _w, _y1], CYAN if _on else (40, 40, 60))
        dr.rectangle([_x, _y0, _x + _w, _y1], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        _lines = wrap_text(_b, font(F_BOLD, 20), _w - 24, dr)
        _ly = (_y0 + _y1) // 2 - (len(_lines) - 1) * 14
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x + _w // 2, _ly + _ln * 28), _line, font(F_BOLD, 20),
                CYAN if _on else DIM, anchor="mm")
        if _i < _lit - 1:
            arrow(dr, _x + _w, (_y0 + _y1) // 2, _x + _w + _gap, (_y0 + _y1) // 2,
                  GREEN if _on else DIM)
    if t > 19:
        txt(dr, (W // 2, 500), 'nothing runs until the event arrives', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 560), 'scale to zero is the whole business model', font(F_SANS, 24), DIM, anchor="mm")
def scene_azdev_keyvault(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["primer"])
    dot_grid(dr)
    bbg_title(dr, 'Key Vault: Secrets Never in Code', CYAN)
    _pts = [(180, 330), (440, 330), (700, 330), (960, 330)]
    _labels = ('managed id', 'request secret', 'audit log', 'cached value')
    _m = len(_pts)
    _prog = clamp((t - 5) / 15)
    _pos = _prog * (_m - 1)
    _i = int(_pos)
    if _i >= _m - 1:
        _i = _m - 2
        _fr = 1.0
    else:
        _fr = _pos - _i
    for _k in range(_m - 1):
        _done = _pos > _k
        dr.line([_pts[_k][0], _pts[_k][1], _pts[_k + 1][0], _pts[_k + 1][1]],
                fill=CYAN if _done else DIM, width=4)
    for _k in range(_m):
        _px, _py = _pts[_k]
        _on = _pos >= _k - 0.001
        dr.ellipse([_px - 26, _py - 26, _px + 26, _py + 26],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_px, _py), str(_k + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_px, _py + 52), _labels[_k], font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    _tx = lerp(_pts[_i][0], _pts[_i + 1][0], _fr)
    _ty = lerp(_pts[_i][1], _pts[_i + 1][1], _fr)
    dr.ellipse([_tx - 13, _ty - 13, _tx + 13, _ty + 13], fill=YELLOW, outline=WHITE, width=2)
    if t > 19:
        txt(dr, (W // 2, 540), 'managed identity is the only credential', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'a secret in git is a secret already burned', font(F_SANS, 24), DIM, anchor="mm")
def scene_azdev_cosmos(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG["3b1b"])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Cosmos DB: Consistency on a Dial', font(F_BOLD, 40), TEAL, anchor="mm")
    txt(dr, (W // 2, 118), 'five levels, one knob', font(F_SANS, 24), DIM, anchor="mm")
    txt(dr, (W // 2, 118), 'consistency × latency × cost', font(F_MONO, 24), DIM, anchor="mm")
    _stats = [('regions', 30, '%d+'), ('p99 read', 10, '%dms'), ('RU/s', 1000000, '%d')]
    _n = len(_stats)
    _w = 1000 // _n
    for _i, (_lb, _tg, _fm) in enumerate(_stats):
        _x = 140 + _i * _w + _w // 2
        _v = _tg * clamp((t - 6 - _i * 2.5) / 6)
        txt(dr, (_x, 320), _fm % int(_v), font(F_MONOB, 50), TEAL, anchor="mm")
        _lines = wrap_text(_lb, font(F_SANS, 22), _w - 24, dr)
        for _ln, _line in enumerate(_lines):
            txt(dr, (_x, 390 + _ln * 30), _line, font(F_SANS, 22), DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 540), 'five levels, one knob — consistency is a dial', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 600), 'RUs are the real schema constraint', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# oracle-oci (bbg x2 + story x1)
def scene_oci_compartments(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'Compartments: The OCI Hierarchy', CYAN)
    _layers = ('workload', 'environment', 'network', 'root tenancy')
    _n = len(_layers)
    _lit = int(clamp((t - 5) / 12) * _n)
    _y0 = (H - _n * 68) // 2 + 60
    for _i, _L in enumerate(_layers):
        _y = _y0 + _i * 68
        _on = _i < _lit
        dr.rectangle([300, _y, 980, _y + 52], fill=(12, 18, 32),
                     outline=CYAN if _on else DIM, width=3 if _on else 2)
        txt(dr, (262, _y + 26), "L%d" % (_n - _i), font(F_MONO, 20), DIM, anchor="rm")
        txt(dr, (640, _y + 26), _L, font(F_BOLD, 23), CYAN if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 612), 'isolation is the default — sharing is explicit', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 660), 'the root compartment is not a junk drawer', font(F_SANS, 24), DIM, anchor="mm")
def scene_oci_vcn(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['bbg'])
    dot_grid(dr)
    bbg_title(dr, 'VCN Topology: Subnets and Gateways', CYAN)
    _nodes = [('vcn', 280, 300), ('public', 560, 200), ('private', 560, 420), ('igw/nat', 900, 300)]
    _edges = [(0, 1), (0, 2), (0, 3), (1, 3)]
    _order = (0, 1, 2, 3)
    _n = int(clamp((t - 5) / 14) * len(_order))
    _seen = set(_order[:_n])
    for _a, _b in _edges:
        _hot = _a in _seen and _b in _seen
        dr.line([_nodes[_a][1], _nodes[_a][2], _nodes[_b][1], _nodes[_b][2]],
                fill=GREEN if _hot else DIM, width=4 if _hot else 3)
    for _i, (_lb, _x, _y) in enumerate(_nodes):
        _on = _i in _seen
        dr.ellipse([_x - 40, _y - 40, _x + 40, _y + 40],
                   fill=CYAN if _on else (16, 16, 30), outline=CYAN, width=3)
        txt(dr, (_x, _y), str(_i + 1), font(F_BOLD, 22), WHITE if _on else DIM, anchor="mm")
        txt(dr, (_x, _y + 58), _lb, font(F_SANS, 20), CREAM if _on else DIM, anchor="mm")
    if t > 19:
        txt(dr, (W // 2, 560), 'route tables are the traffic cops', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 616), 'packets vanish where routes disagree', font(F_SANS, 24), DIM, anchor="mm")
def scene_oci_alwaysfree(t, dr, img):
    dr.rectangle([0, 0, W, H], fill=STYLE_BG['story'])
    dot_grid(dr)
    txt(dr, (W // 2, 70), 'Always Free: The Generous Tier', font(F_BOLD, 40), GOLD, anchor="mm")
    txt(dr, (W // 2, 118), 'two VMs, forever, no credit card drama', font(F_SERIF, 24), DIM, anchor="mm")
    _items = [('compute', 1.0, '2 VMs', GREEN), ('block storage', 1.0, '200 GB', TEAL), ('autonomous db', 1.0, '2 DBs', YELLOW), ('outbound data', 0.5, '10 TB', ORANGE)]
    for _i, (_lb, _fr, _vl, _cl) in enumerate(_items):
        _y = 215 + _i * 80
        _here = t > 5 + _i * 2.4
        _f = clamp((t - 5 - _i * 2.4) / 2.5) * _fr if _here else 0.0
        bar(dr, 400, _y, 520, 38, _f, _cl, label=_lb, val=_vl if _here else None)
    if t > 19:
        txt(dr, (W // 2, 622), 'two VMs, forever — no credit card drama', font(F_SANS, 25), CREAM, anchor="mm")
    if t > 23:
        txt(dr, (W // 2, 664), 'the cheapest cloud is the one you never pay for', font(F_SANS, 24), DIM, anchor="mm")
# ============================================================
# registry
SLUG_DIR = {
    'clf': 'aws-clf',
    'data': 'aws-data',
    'dop': 'aws-dop',
    'ml': 'aws-ml',
    'saa': 'aws-saa',
    'scs': 'aws-scs',
    'soa': 'aws-soa',
    'az104': 'az-104',
    'az305': 'az-305',
    'az700': 'az-700',
    'azdev': 'azure-developer',
    'oci': 'oracle-oci',
}
def V(kicker, short, slug, title, sub, style, scene, blurb, captions):
    return dict(file="bc-%s-%s.mp4" % (style, slug), style=style, scene=scene,
                kicker=kicker, title=title, sub=sub,
                bootcamp=SLUG_DIR[short],
                blurb=blurb, captions=captions)

BOOTCAMP_K = {
    'clf': 'AWS CLF · Cloud Practitioner',
    'data': 'AWS DATA · Data Engineer',
    'dop': 'AWS DOP · DevOps Engineer Pro',
    'ml': 'AWS ML · Machine Learning Specialty',
    'saa': 'AWS SAA · Solutions Architect',
    'scs': 'AWS SCS · Security Specialty',
    'soa': 'AWS SOA · SysOps Administrator',
    'az104': 'AZ-104 · Azure Administrator',
    'az305': 'AZ-305 · Azure Architect Expert',
    'az700': 'AZ-700 · Azure Network Engineer',
    'azdev': 'AZURE DEV · Azure Developer',
    'oci': 'OCI · Oracle Cloud Infrastructure',
}
VIDEOS = [
 # --- aws-clf
 V(BOOTCAMP_K['clf'], 'clf', 'aws-clf-shared', 'Shared Responsibility: Who Patches What',
   'the line between AWS and you', 'bbg', scene_aws_clf_shared,
   'The shared responsibility model: AWS secures the cloud itself — hardware, network, virtualization — while you secure what is IN the cloud: data, IAM, OS patches. Know the line before the exam draws it.',
   [(4,10,'AWS owns the cloud itself: facilities, hardware, network'),
    (10,16,'AWS owns virtualization: hypervisor, managed services'),
    (16,22,'You own what is IN the cloud: data, IAM, OS patches'),
    (22,26,'Draw the line first — every CLF question tests it')]),
 V(BOOTCAMP_K['clf'], 'clf', 'aws-clf-pricing', 'Pay-As-You-Go: Three Ways to Pay',
   'on-demand vs reserved vs spot', '3b1b', scene_aws_clf_pricing,
   'Three EC2 pricing models: on-demand at full price, reserved at 40% off for a 1-year promise, spot at 70% off for interruptible spare capacity. Match the model to the workload or burn budget.',
   [(4,10,'On-demand: full price, zero commitment, always available'),
    (10,16,'Reserved: 40% off for a one-year promise'),
    (16,22,'Spot: 70% off spare capacity — interruptible'),
    (22,26,'Steady workloads go reserved — batch goes spot')]),
 V(BOOTCAMP_K['clf'], 'clf', 'aws-clf-global', 'Regions and AZs: The Global Map',
   'deploy close, survive failure', 'bbg', scene_aws_clf_global,
   'AWS regions are geographic areas; each holds multiple Availability Zones — isolated data centers with independent power. Deploy across AZs to survive a data-center failure, across regions to survive a disaster.',
   [(4,10,'A region: a geographic area, like us-east-1'),
    (10,16,'Each region holds isolated Availability Zones'),
    (16,22,'AZs: separate power, separate fate'),
    (22,26,'Multi-AZ survives failure — multi-region survives disaster')]),
 # --- aws-data
 V(BOOTCAMP_K['data'], 'data', 'aws-data-pipeline', 'The Data Pipeline: S3 to Insight',
   'raw events in, dashboards out', 'bbg', scene_aws_data_pipeline,
   'A modern data pipeline: Kinesis streams the events, S3 lands them raw, Glue catalogs and transforms, Redshift warehouses, QuickSight visualizes. Five stages, one flow, zero servers to babysit.',
   [(4,10,'Kinesis streams millions of events per second'),
    (10,16,'S3 lands everything raw — the data lake'),
    (16,22,'Glue catalogs and transforms — ETL without servers'),
    (22,26,'Redshift warehouses — QuickSight visualizes')]),
 V(BOOTCAMP_K['data'], 'data', 'aws-data-zones', 'Lake Zones: Raw to Curated',
   'governance grows as data refines', 'bbg', scene_aws_data_zones,
   'Data lake zones: raw lands untouched, cleansed fixes schemas, curated serves analytics-ready tables. Governance tightens as you rise — raw is a swamp, curated is a product.',
   [(4,10,'Raw zone: land everything untouched — the swamp'),
    (10,16,'Cleansed zone: schemas fixed, types coerced'),
    (16,22,'Curated zone: analytics-ready, governed, trusted'),
    (22,26,'Governance tightens as you rise')]),
 V(BOOTCAMP_K['data'], 'data', 'aws-data-stream', 'Streaming ETL in 100 Seconds',
   'window, aggregate, sink', 'fireship', scene_aws_data_stream,
   'A streaming ETL sketch: read the Kinesis shard, window events by minute, aggregate the counts, sink to S3. Four verbs, infinite data — the window is what makes streaming sane.',
   [(4,10,'Read the shard — the stream never ends'),
    (10,16,'Window by event time — one-minute buckets'),
    (16,22,'Aggregate inside each window — counts, sums'),
    (22,26,'Sink to S3 — the window makes streaming sane')]),
 # --- aws-dop
 V(BOOTCAMP_K['dop'], 'dop', 'aws-dop-pipeline', 'The Delivery Pipeline',
   'commit to production without fear', 'bbg', scene_aws_dop_pipeline,
   'The DevOps pipeline: CodeCommit holds the source, CodeBuild compiles and tests, CodeDeploy rolls out in waves. Every commit rides the same conveyor — manual deploys are how outages are born.',
   [(4,10,'CodeCommit: the source of truth — every change starts here'),
    (10,16,'CodeBuild: compile, test, package — the gate'),
    (16,22,'CodeDeploy: rolling waves — no big-bang releases'),
    (22,26,'One conveyor from commit to prod — no manual steps')]),
 V(BOOTCAMP_K['dop'], 'dop', 'aws-dop-bluegreen', 'Blue/Green: The Zero-Downtime Swap',
   'two environments, one router flip', 'primer', scene_aws_dop_bluegreen,
   'Blue/green deployment: blue serves traffic while green gets the new build; tests pass on green, the router flips, blue becomes the standby. Rollback is another flip — sixty seconds, not sixty minutes.',
   [(4,10,'Blue serves live traffic — green takes the new build'),
    (10,16,'Tests run against green — production untouched'),
    (16,22,'Router flips — green is live in seconds'),
    (22,26,'Rollback is just another flip — 60 seconds')]),
 V(BOOTCAMP_K['dop'], 'dop', 'aws-dop-cfn', 'CloudFormation in 100 Seconds',
   'infrastructure you can diff', 'fireship', scene_aws_dop_cfn,
   'A CloudFormation template: parameters at the top, resources in the middle, outputs at the bottom. The stack is the unit of deployment — diff it, review it, then create the change set.',
   [(4,10,'Parameters: the knobs — environment, instance type'),
    (10,16,'Resources: the what — declared, not clicked'),
    (16,22,'Outputs: the answers — export what others need'),
    (22,26,'The stack deploys as one unit — or rolls back as one')]),
 # --- aws-ml
 V(BOOTCAMP_K['ml'], 'ml', 'aws-ml-sagemaker', 'SageMaker: Train, Tune, Deploy',
   'the ML assembly line', 'bbg', scene_aws_ml_sagemaker,
   'The SageMaker loop: training jobs learn from S3 data, tuning jobs search hyperparameters, endpoints serve predictions. Experiments track in the registry — the model that ships is the one you can reproduce.',
   [(4,10,'Training jobs learn from S3 — compute scales out'),
    (10,16,'Tuning searches hyperparameters — Bayesian, not guessing'),
    (16,22,'Endpoints serve predictions — autoscaled inference'),
    (22,26,'The registry tracks every experiment — reproduce or it did not happen')]),
 V(BOOTCAMP_K['ml'], 'ml', 'aws-ml-bias', 'Bias Metrics: Count What Matters',
   'fairness is a measurement problem', 'primer', scene_aws_ml_bias,
   'Bias in ML is a measurement problem: selection rate by group, false-positive gaps, calibration drift. Count the disparities before you ship — the exam and the auditors both ask for the numbers.',
   [(4,10,'Selection rate per group — the first disparity check'),
    (10,16,'False-positive gaps — who pays for the errors'),
    (16,22,'Calibration drift — scores must mean the same everywhere'),
    (22,26,'Count it before you ship — auditors ask for numbers')]),
 V(BOOTCAMP_K['ml'], 'ml', 'aws-ml-gradient', 'Gradient Descent: Walking Downhill',
   'the learning rate is the stride', '3b1b', scene_aws_ml_gradient,
   'Gradient descent: compute the slope of the loss, step against it, repeat ten thousand times. Too big a step overshoots the valley; too small takes forever — the learning rate is the stride length.',
   [(4,10,'Loss is a landscape — the model stands on a hill'),
    (10,16,'Compute the gradient — the downhill direction'),
    (16,22,'Step against it — repeat ten thousand times'),
    (22,26,'Learning rate: too big overshoots — too small crawls')]),
 # --- aws-saa
 V(BOOTCAMP_K['saa'], 'saa', 'aws-saa-arch', 'Three-Tier Architecture',
   "the exam's favorite diagram", 'bbg', scene_aws_saa_arch,
   'The classic three-tier web architecture: Route 53 routes, the ALB balances, EC2 in an Auto Scaling group computes, RDS Multi-AZ persists. Stateless in front, stateful behind — scale the tiers independently.',
   [(4,10,'Route 53 routes — DNS with health checks'),
    (10,16,'ALB balances — traffic spreads, instances stay dumb'),
    (16,22,'Auto Scaling group computes — stateless, replaceable'),
    (22,26,'RDS Multi-AZ persists — the stateful heart')]),
 V(BOOTCAMP_K['saa'], 'saa', 'aws-saa-failover', 'Multi-AZ Failover: Surviving the Fire',
   'the standby is already warm', 'bbg', scene_aws_saa_failover,
   'RDS Multi-AZ keeps a synchronous standby in another zone; when the primary fails, DNS flips and the standby promotes in about a minute. The exam loves the RTO number — know it cold.',
   [(4,10,'Primary serves writes in AZ-a — standby syncs in AZ-b'),
    (10,16,'Failure detected — automated, no human paged'),
    (16,22,'DNS flips to the standby — promotion in ~60 seconds'),
    (22,26,'RTO ~1 minute, RPO ~zero — know the numbers cold')]),
 V(BOOTCAMP_K['saa'], 'saa', 'aws-saa-s3tiers', 'S3 Storage Classes: Pay for Access',
   'hot data, cold price', '3b1b', scene_aws_saa_s3tiers,
   'S3 storage classes price access patterns: Standard for hot data, Intelligent-Tiering for the unknown, Glacier Instant for quarterly reads, Deep Archive for the compliance vault. Lifecycle rules move objects down automatically.',
   [(4,10,'Standard: hot data — millisecond access, top price'),
    (10,16,'Intelligent-Tiering: unknown patterns — auto-optimizes'),
    (16,22,'Glacier: quarterly reads — minutes to retrieve'),
    (22,26,'Deep Archive: the compliance vault — $1/TB/month')]),
 # --- aws-scs
 V(BOOTCAMP_K['scs'], 'scs', 'aws-scs-iam', 'IAM Policy Evaluation: The Gauntlet',
   'explicit deny always wins', 'bbg', scene_aws_scs_iam,
   'IAM evaluation order: explicit deny wins over everything, then explicit allow, then default deny. SCPs, identity policies, and resource policies all vote — one deny anywhere kills the request.',
   [(4,10,'Explicit deny — wins over everything, always'),
    (10,16,'Explicit allow — needed from identity OR resource'),
    (16,22,'Default deny — silence means no'),
    (22,26,'One deny anywhere — SCP, identity, or resource — kills it')]),
 V(BOOTCAMP_K['scs'], 'scs', 'aws-scs-kms', 'Envelope Encryption: Keys Protect Keys',
   'the data key never travels far', 'primer', scene_aws_scs_kms,
   'Envelope encryption: KMS guards the master key, a unique data key encrypts each object, and the encrypted data key rides alongside. Decrypt the envelope first, then the data — the master key never leaves KMS.',
   [(4,10,'KMS holds the master key — it never leaves'),
    (10,16,'A unique data key encrypts each object'),
    (16,22,'The encrypted data key rides with the object'),
    (22,26,'Decrypt envelope first — then the data')]),
 V(BOOTCAMP_K['scs'], 'scs', 'aws-scs-guardduty', 'GuardDuty Findings in 100 Seconds',
   'read the finding, not the panic', 'fireship', scene_aws_scs_guardduty,
   'A GuardDuty finding is JSON with a severity, a type, and the evidence: which instance, which port, which threat list. Read the finding fields before you page anyone — severity 8+ means act now.',
   [(4,10,'Findings are JSON — severity, type, evidence'),
    (10,16,'The resource block names the compromised instance'),
    (16,22,'Threat intel lists explain WHY it fired'),
    (22,26,'Severity 8+ — act now; below that, triage in the morning')]),
 # --- aws-soa
 V(BOOTCAMP_K['soa'], 'soa', 'aws-soa-scaling', 'Auto Scaling: Breathe With Demand',
   'scale out fast, scale in slow', 'bbg', scene_aws_soa_scaling,
   'Auto Scaling: CloudWatch alarms fire, the group adds instances in minutes, cools down, then removes them slowly. Scale out fast on the spike — scale in slow to avoid flapping.',
   [(4,10,'CloudWatch alarm fires — CPU over 70%'),
    (10,16,'Scale out: add instances in minutes'),
    (16,22,'Cooldown: let the new capacity settle'),
    (22,26,'Scale in slow — flapping costs more than idle')]),
 V(BOOTCAMP_K['soa'], 'soa', 'aws-soa-alarms', 'CloudWatch Alarms: Eyes Everywhere',
   'alarm on symptoms, not causes', 'primer', scene_aws_soa_alarms,
   'CloudWatch alarms: metrics stream in, thresholds evaluate, SNS notifies, and Systems Manager can remediate automatically. Alarm on symptoms users feel — latency, errors — not on causes you guess.',
   [(4,10,'Metrics stream every minute — the vital signs'),
    (10,16,'Thresholds evaluate — breach for N periods'),
    (16,22,'SNS notifies — the page goes out'),
    (22,26,'SSM remediates — restart, then tell a human')]),
 V(BOOTCAMP_K['soa'], 'soa', 'aws-soa-backup', 'The 3 AM Restore',
   'backups are tested restores', 'story', scene_aws_soa_backup,
   'A restore runbook: detect the corruption, locate the last good snapshot, restore to a sandbox, verify the data, then cut over. Backups are worthless until a restore has been rehearsed — test it quarterly.',
   [(4,10,'Detect the corruption — the 3 AM page'),
    (10,16,'Locate the last good snapshot'),
    (16,22,'Restore to a sandbox — verify before prod'),
    (22,26,'Cut over — RTO met, back to sleep')]),
 # --- az-104
 V(BOOTCAMP_K['az104'], 'az104', 'az104-rbac', 'RBAC Scopes: Who Can Touch What',
   'deny assignments beat everything', 'bbg', scene_az104_rbac,
   'Azure RBAC: permissions flow down from management group to subscription to resource group to resource — and deny assignments override every allow. Scope narrow, grant least privilege, audit with Access Reviews.',
   [(4,10,'Management group: the top of the inheritance chain'),
    (10,16,'Subscription and resource group: scopes narrow downward'),
    (16,22,'Role assignments grant — Reader, Contributor, Owner'),
    (22,26,'Deny assignments override everything — least privilege wins')]),
 V(BOOTCAMP_K['az104'], 'az104', 'az104-vnet', 'VNet Peering: The Private Highway',
   'no public internet, no problem', 'bbg', scene_az104_vnet,
   "VNet peering connects virtual networks over Microsoft's backbone — low latency, no public internet. Gateway transit lets spokes share one VPN gateway; peering is non-transitive by design.",
   [(4,10,'Two VNets peer over the Microsoft backbone'),
    (10,16,'Private traffic — never touches the public internet'),
    (16,22,'Gateway transit: spokes share one VPN gateway'),
    (22,26,'Peering is non-transitive — hub-and-spoke needs planning')]),
 V(BOOTCAMP_K['az104'], 'az104', 'az104-arm', 'ARM Templates in 100 Seconds',
   'declare the end state', 'fireship', scene_az104_arm,
   'An ARM template declares the end state: parameters in, resources defined, outputs out. Deployments are idempotent — run it twice, get the same infrastructure. What-if shows the diff before anything changes.',
   [(4,10,'Parameters: the inputs — names, SKUs, locations'),
    (10,16,'Resources: declared end state — not a script'),
    (16,22,'Idempotent: run it twice — same result'),
    (22,26,'What-if first — read the diff, then deploy')]),
 # --- az-305
 V(BOOTCAMP_K['az305'], 'az305', 'az305-landing', 'Landing Zones: The Enterprise Foundation',
   'design for 500 subscriptions, not 5', 'bbg', scene_az305_landing,
   'An Azure landing zone: management groups for hierarchy, policy for guardrails, hub networking for shared services, identity as the perimeter. Design for five hundred subscriptions on day one — refactoring foundations later is agony.',
   [(4,10,'Management groups: hierarchy before anything'),
    (10,16,'Policy guardrails: allowed regions, required tags'),
    (16,22,'Hub networking: firewall, DNS, VPN in one place'),
    (22,26,'Identity is the perimeter — design for 500 subscriptions')]),
 V(BOOTCAMP_K['az305'], 'az305', 'az305-paired', 'Paired Regions: Surviving the Outage',
   'the pair is 300 miles apart for a reason', 'bbg', scene_az305_paired,
   'Azure region pairs sit at least 300 miles apart and update one at a time — platform updates never hit both. Zone-redundant services survive a datacenter loss; paired-region failover survives the big one.',
   [(4,10,'Region pairs: 300+ miles apart — blast radius contained'),
    (10,16,'Platform updates roll one region at a time'),
    (16,22,'Zone redundancy survives a datacenter loss'),
    (22,26,'Paired failover survives the regional event')]),
 V(BOOTCAMP_K['az305'], 'az305', 'az305-cost', "Cost Optimization: The Architect's Levers",
   'every design decision has a price tag', '3b1b', scene_az305_cost,
   'Cost levers the architect pulls: right-size the VMs, reserve the steady state, auto-scale the peaks, tier the storage, delete the orphans. A design without a cost model is a wish.',
   [(4,10,'Right-size: kill the 4% CPU monsters'),
    (10,16,'Reserve steady state — 40% off for commitment'),
    (16,22,'Auto-scale the peaks — pay for the spike only'),
    (22,26,'Tier storage, delete orphans — the janitor lever')]),
 # --- az-700
 V(BOOTCAMP_K['az700'], 'az700', 'az700-dns', 'DNS Resolution: The 100ms That Matters',
   'every click starts with a lookup', 'primer', scene_az700_dns,
   'DNS resolution: the stub asks the resolver, the resolver walks root to TLD to authoritative, the answer caches at every step. Private DNS zones keep VNet names off the public internet.',
   [(4,10,'The stub resolver asks — every click starts here'),
    (10,16,'Walk the hierarchy: root, TLD, authoritative'),
    (16,22,'Answers cache at every step — TTL is the timer'),
    (22,26,'Private zones: VNet names stay off the public internet')]),
 V(BOOTCAMP_K['az700'], 'az700', 'az700-vwan', 'Virtual WAN: Hub-and-Spoke at Scale',
   'one hub, fifty spokes, zero mesh headaches', 'bbg', scene_az700_vwan,
   'Azure Virtual WAN: a managed hub with routing, firewall, and VPN baked in; spokes peer to the hub, never to each other. One hub, fifty spokes, zero mesh headaches.',
   [(4,10,'The vWAN hub: routing, firewall, VPN — managed'),
    (10,16,'Spokes peer to the hub — never spoke-to-spoke'),
    (16,22,'Branch offices ride ExpressRoute or VPN into the hub'),
    (22,26,'One routing table to rule the topology')]),
 V(BOOTCAMP_K['az700'], 'az700', 'az700-nsg', 'NSG Rules in 100 Seconds',
   'lowest number wins', 'fireship', scene_az700_nsg,
   'NSG rules evaluate by priority number — lowest first, first match wins, default deny at the end. Allow the app port high in the list, leave the defaults alone, and log the denies to find the typo.',
   [(4,10,'Priority numbers: lowest evaluates first'),
    (10,16,'First match wins — order is the policy'),
    (16,22,'Default deny-all sits at the bottom, untouchable'),
    (22,26,'Flow logs show the denies — the typo confesses')]),
 # --- azure-developer
 V(BOOTCAMP_K['azdev'], 'azdev', 'azdev-functions', 'Serverless Triggers: Code That Waits',
   'nothing runs until the event arrives', 'bbg', scene_azdev_functions,
   'Azure Functions: HTTP triggers serve APIs, queue triggers chew backlogs, timer triggers run the cron, blob triggers react to uploads. Nothing runs until the event arrives — then it scales to zero cost again.',
   [(4,10,'HTTP trigger: the API endpoint without a server'),
    (10,16,'Queue trigger: chew the backlog one message at a time'),
    (16,22,'Timer trigger: cron without the VM'),
    (22,26,'Blob trigger: react to every upload — scale to zero after')]),
 V(BOOTCAMP_K['azdev'], 'azdev', 'azdev-keyvault', 'Key Vault: Secrets Never in Code',
   'managed identity is the only credential', 'primer', scene_azdev_keyvault,
   'The Key Vault flow: the app authenticates with its managed identity — no stored credential — requests the secret, gets the value, caches briefly. Secrets never in code, never in config, rotation without redeploys.',
   [(4,10,'Managed identity: the app IS the credential'),
    (10,16,'No passwords stored anywhere — nothing to leak'),
    (16,22,'Request the secret — audit-logged every time'),
    (22,26,'Rotate in the vault — no redeploy needed')]),
 V(BOOTCAMP_K['azdev'], 'azdev', 'azdev-cosmos', 'Cosmos DB: Consistency on a Dial',
   'five levels, one knob', '3b1b', scene_azdev_cosmos,
   "Cosmos DB's five consistency levels dial the trade between correctness and speed: strong, bounded staleness, session, consistent prefix, eventual. Request units price every operation — model the RU cost before the data model.",
   [(4,10,'Strong: linearizable — slowest, safest'),
    (10,16,'Session: your writes, your reads — the sweet spot'),
    (16,22,'Eventual: fastest — replicas converge later'),
    (22,26,'RUs price everything — model cost before schema')]),
 # --- oracle-oci
 V(BOOTCAMP_K['oci'], 'oci', 'oci-compartments', 'Compartments: The OCI Hierarchy',
   'isolation is the default', 'bbg', scene_oci_compartments,
   'OCI compartments: a nested hierarchy where every resource lives in exactly one compartment, policies attach at any level, and quotas contain blast radius. Isolation is the default — sharing is the explicit choice.',
   [(4,10,'Every resource lives in exactly one compartment'),
    (10,16,'Nesting: prod, dev, and network each walled off'),
    (16,22,'Policies attach at any level — inherit downward'),
    (22,26,'Quotas per compartment — blast radius contained')]),
 V(BOOTCAMP_K['oci'], 'oci', 'oci-vcn', 'VCN Topology: Subnets and Gateways',
   'route tables are the traffic cops', 'bbg', scene_oci_vcn,
   'An OCI VCN: public subnets route through the internet gateway, private subnets through the NAT or service gateway, and security lists filter at the subnet edge. Route tables are the traffic cops — read them first when packets vanish.',
   [(4,10,'VCN: your private network slice — /16 of your own'),
    (10,16,'Public subnets → internet gateway'),
    (16,22,'Private subnets → NAT or service gateway'),
    (22,26,'Security lists filter at the subnet edge')]),
 V(BOOTCAMP_K['oci'], 'oci', 'oci-alwaysfree', 'Always Free: The Generous Tier',
   'two VMs, forever, no credit card drama', 'story', scene_oci_alwaysfree,
   'OCI Always Free: two AMD VMs, 200 GB of block storage, and an autonomous database — forever, not a trial. The exam loves the always-free list; the architect loves a free lab that never expires.',
   [(4,10,'Two AMD VMs — forever, not a 12-month trial'),
    (10,16,'200 GB block storage — real disks, $0'),
    (16,22,'Autonomous Database — the self-driving tier, free'),
    (22,26,"A lab that never expires — learn on Oracle's dime")]),
]
# ============================================================ render loop (mirrors gen_bootcamp_b4)
def render_video(v):
    fname = v["file"]
    path = os.path.join(OUT, fname)
    style, scene = v["style"], v["scene"]
    accent = ACCENTS[style]
    caps = sorted(v["captions"])
    def frames():
        total = int(NFR / 8) if SMOKE else NFR
        for f in range(total):
            t = f / FPS
            img = Image.new("RGB", (W, H), STYLE_BG[style])
            dr = ImageDraw.Draw(img)
            if t < 4:
                title_card(dr, style, v["kicker"], v["title"], v["sub"], t)
            elif t < 26:
                scene(t, dr, img)
                cur = next((c for a, b, c in caps if a <= t < b), None)
                if cur:
                    caption_bar(dr, cur, accent)
            else:
                end_card(dr, style, v["title"], v["kicker"], t - 26)
            preview_tag(dr)
            yield img
            if f % 180 == 0:
                print("  %s frame %d/%d" % (fname, f, total), flush=True)
    encode_video(path, frames())
    base, _ = os.path.splitext(path)
    vtt_cues = [(4.0, 10.0, "Preview \u2014 narration coming. " + caps[0][2])]
    vtt_cues += [(float(a), float(b), c) for a, b, c in caps]
    vtt_cues.append((26.0, 30.0, "Preview ends. Full voiceover ships when TTS is restored."))
    write_vtt(base + ".vtt", vtt_cues)
    write_narration(base + ".narration.md", v["title"], v["kicker"], fname, caps, v["blurb"])
    sz = os.path.getsize(path)
    print("DONE %s (%d bytes)" % (fname, sz), flush=True)
    return fname, sz

def main():
    only = sys.argv[1:] or None
    vids = [v for v in VIDEOS if (only is None or v["file"] in only or v["file"].replace(".mp4", "") in only)]
    print("Rendering %d videos (SMOKE=%s)" % (len(vids), SMOKE), flush=True)
    for v in vids:
        print("START", v["file"], flush=True)
        try:
            render_video(v)
        except Exception as e:
            print("FAILED %s: %r" % (v["file"], e), flush=True)

if __name__ == "__main__":
    main()
