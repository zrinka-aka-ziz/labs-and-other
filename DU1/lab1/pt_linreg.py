import torch
import torch.optim as optim


def mean_square_loss(Y, Y_):
    return torch.mean((Y_ - Y) ** 2)

## Definicija  grafa
# podaci i parametri, inic parametara
a = torch.randn(1, requires_grad=True)
b = torch.randn(1, requires_grad=True)

X = torch.tensor([1, 2])
Y = torch.tensor([3, 5])

# optimizer: gradijentni spust
optimizer = optim.SGD([a, b], lr=0.1)

for i in range(100):
    # afin regresijski model
    Y_ = a*X + b

    # kvadratni gubitak
    loss = mean_square_loss(Y, Y_)

    # gradijenat račun
    loss.backward()

    # optimizer step
    optimizer.step()
    diffs = Y_ - Y
    a_grad_manual = 2 * torch.mean(diffs * X)
    b_grad_manual = 2 * torch.mean(diffs)
    print(f'step: {i}, loss:{loss}, Y_:{Y_}\n'
          f'a:{a}, a_grad:{a.grad}, a_grad_manual: {a_grad_manual:.04f}\n '
          f'b:{b}, b_grad:{b.grad}, b_grad_manual: {b_grad_manual:.04f}')

    # Postavljanje gradijenata na nulu
    optimizer.zero_grad()
