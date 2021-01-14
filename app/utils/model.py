from mmdet.apis import inference_detector, init_detector, show_result_pyplot, show_result_pyplot
import requests
from os import chdir, system, path

def get_model(weights, config):

    system('mkdir -p model_config')

    weights_path = f"model_config/{weights.split('/')[-1]}"
    if not path.exists(weights_path):
      url = f'{weights}'
      r = requests.get(url)
      open(weights_path, 'wb').write(r.content)

    return 'Model donloaded!'

def run_model(img,
              weights='https://open-mmlab.s3.ap-northeast-2.amazonaws.com/mmdetection/v2.0/mask_rcnn/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco/mask_rcnn_r50_caffe_fpn_mstrain-poly_3x_coco_bbox_mAP-0.408__segm_mAP-0.37_20200504_163245-42aa3d00.pth',
              config='src/mmdetection/configs/mask_rcnn/mask_rcnn_r50_caffe_fpn_1x_coco.py'):
    
    get_model(weights, config)
    weights_path = f"model_config/{weights.split('/')[-1]}"
    print(config_path, weights_path)
    model = init_detector(config, weights_path, device='cpu')
    # Use the detector to do inference
    result = inference_detector(model, img)

    return model, result