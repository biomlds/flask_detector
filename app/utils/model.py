import requests
from os import chdir, system, path
from mmdet.apis import inference_detector, init_detector, show_result_pyplot, show_result_pyplot

def run_model(img, processed_filename, processed_img,
              weights='model_configs/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth',
              config='../mmdetection/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_1x_coco.py'):
    model = init_detector(config, weights, device='cpu')
    result = inference_detector(model, img)

    model.show_result(img, result, score_thr=0.5, show=False,
                win_name=processed_filename,
                out_file=processed_img)