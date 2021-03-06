from pytorch.network import Unet
from pytorch.dataset import CustomDataset
import torch
import os
import numpy as np
from torch.utils.data import DataLoader
from tensorboardX import SummaryWriter
import argparse

torch.set_printoptions(profile='full')
if __name__ == '__main__':

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    print("Default path : " + os.getcwd())
    parser.add_argument("--model_dir",
                        help="Directory of pre-trained model, you can download at \n"
                             "https://drive.google.com/drive/folders/1s4M-_SnCPMj_2rsMkSy3pLnLQcgRakAe?usp=sharing")
    parser.add_argument('-img', '--image_dir', help='Directory of your test_image ""folder""', default='test')
    parser.add_argument('--cuda', help="cuda for cuda, cpu for cpu, default = cuda", default='cuda')
    parser.add_argument('--batch_size', help="batchsize, default = 4", default=4, type=int)
    parser.add_argument('--logdir', help="logdir, default = pytorch/log/Image_test", default='pytorch/log/Image_test')
    args = parser.parse_args()

    print(args)
    print(os.getcwd())
    device = torch.device(args.cuda)
    # args.model_dir = 'models/state_dict/07121619/0epo_1000step.ckpt'
    state_dict = torch.load(args.model_dir, map_location=args.cuda)
    # state_dict = torch.load(model_dir)
    model = Unet().to(device)
    model.load_state_dict(state_dict)
    custom_dataset = CustomDataset(root_dir=args.image_dir)
    dataloader = DataLoader(custom_dataset, args.batch_size, shuffle=False)
    writer = SummaryWriter(args.logdir)
    model.eval()
    for i, batch in enumerate(dataloader):
        img = batch.to(device)
        # mask = batch['mask'].to(device)
        with torch.no_grad():
            pred, loss = model(img)
        pred = pred[5].data
        pred.requires_grad_(False)
        writer.add_image(args.model_dir + ', img', img, i)
        writer.add_image(args.model_dir + ', mask', pred, i)
    writer.close()
