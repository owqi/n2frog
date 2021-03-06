from numpy import roll, size, fliplr, tril, triu, conj, ceil, outer, dot
from numpy.fft import fft, ifft, ifftshift, fftshift
from scipy.sparse.linalg import svds
from numpy.linalg import norm

def makePulse(electricFROG, lastPulse, whichMethod):

    N = size(electricFROG, 1)

    #Do the exact inverse of the procedure in makeFROG...
    #Undo the line: EF=circshift(fft(EF,[],1),ceil(N/2)-1);
    electricFROG = ifft(roll(electricFROG, int(-ceil(N/2))), axis=1)

    #Undo the line: EF=fliplr(fftshift(EF,2));
    electricFROG = ifftshift(fliplr(electricFROG), 1)

    #Undo the lines: for n=2:N  EF(n,:) = circshift(EF(n,:), [0 1-n]);  end
    for n in range(1, N):
        electricFROG[n, :] = roll(electricFROG[n, :], n)

    # Now EF is the "outer product form", see Kane1999.
    # Anti-alias in time domain. See makeFROG for explanation.
    electricFROG = electricFROG - tril(electricFROG, int(-ceil(N/2))) - triu(electricFROG, int(ceil(N/2)));

    #if (whichMethod == 0): # power method
    #electricFROG*conj(electricFROG.T)
    #outputPulse = lastPulse*(electricFROG@conj(electricFROG.T))
    #tempouter = outer(electricFROG, electricFROG)
    #TODO MEMORY ERROR
    outputPulse = dot(outer(electricFROG, conj(electricFROG)),lastPulse)
    #else: # SVD method
    #    [U, S, V] = svds(electricFROG, 1)
    #    outputPulse = U[:,0]

    # normalize to Euclidean norm 1
    outputPulse = outputPulse/norm(outputPulse)

    return outputPulse
