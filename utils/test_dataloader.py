import time

from datasets import get_brats_dataloader
from tqdm import tqdm
from swap_dimensions import swap_batch_slice_dimensions
from visualization import show_mask_origin

if __name__ == '__main__':
    root_dir = "E:\Work\dataset\ASNR-MICCAI-BraTS2023-GLI-Challenge-TrainingData"
    root_dir_2060 = "D:\Project\dataset\ASNR-MICCAI-BraTS2023-GLI-Challenge-TrainingData"
    slice_deep = 128
    batch_size = 1
    batch_slice = 16

    index = 0
    dataloader = get_brats_dataloader(root_dir=root_dir, batch_size=batch_size, slice_deep=128, slice_size=192,
                                      mask_kernel_size=3, binary_mask='1000', mask_rate=0.75,
                                      num_workers=4, mode='test')
    loop = 2
    total = 1251 * batch_size
    total_slice = 1251 * 128
    print("Total: ", total)
    current = 0

    start = time.time()
    for epoch in range(100):
        with tqdm(dataloader, desc=f"Epoch {epoch + 1}/100", unit="batch") as pbar:
            for x, y in pbar:
                x_swap = swap_batch_slice_dimensions(x)
                y_swap = swap_batch_slice_dimensions(y)
                i = 0
                for step in range(slice_deep // batch_slice):

                    x_step = x_swap[range(step, x_swap.shape[0], slice_deep // batch_slice), :, :, :]
                    y_step = y_swap[range(step, y_swap.shape[0], slice_deep // batch_slice), :, :, :]
                    current += batch_slice
                    pbar.set_description(
                        f"Epoch {epoch + 1}/100; Slice current {batch_slice * (step + 1)}/{slice_deep};"
                        f"Slice total {current}/{total_slice}")

                    # print("Step: ", step)
                    # print(x.shape, y.shape)
                    # show_mask_origin(x_step, y_step, index)
                    # if i == loop:
                    #     break
                    # i += 1

    end = time.time()
    print("Time: ", end - start)

    print("Current: ", current)
