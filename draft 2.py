import numpy as np
import skimage as ski
import matplotlib.pyplot as plt

#0 would be susceptible; 1 would be recovered 2 would be vaccinated 3+ would be infected; 6 would go back to recovered

def evolve(neighborhood):
    max_days = 17
    if neighborhood[1,1] == max_days:
        return 1
    elif neighborhood[1,1] == 1:
        return 1
    elif neighborhood[1,1] > 2:
        return neighborhood[1,1]+1
    else: 
        p_sick = 0.25
        p_well = (1-p_sick)**(neighborhood > 2).sum()
        if p_well > np.random.uniform(0,1):
            return 0
        else: 
            return 2
        
    
def edges(image):

    image[0,:] = image[-2,:]
    image[-1,:] = image[1,:]
    image[:,0] = image[:,-2]
    image[:,-1] = image[:,1]
    return image

if __name__ == "__main__":
    # Set image size
    rows = 50
    cols = 50
    people = rows * cols
    
    # Generate random array and the wrap
    #img = np.uint8(np.random.randint(0, 2, [rows, cols], dtype=np.uint8))
    #img = edges(img)
    img = np.uint8(np.zeros([rows, cols]))
    img[1, 2] = 3
    img[2, 3] = 3
    img[3, 1] = 3
    img[3, 2] = 3
    img[3, 3] = 3
    # Display original random image
    plt.figure(num=1, clear=True)
    plt.imshow(img, vmin=0, vmax=5)
    plt.pause(0.01)    
    
    # Display original random image and
    # Assign it to a variable for animation
    plt.figure(num=2, clear=True)
    anim = plt.imshow(img, vmin=0, vmax=5)
    plt.pause(0.01)     
    
    # Evolve image up to N times
    S, I, R, V = [rows * cols - 5], [5], [0], [0]
        
    days = 2000
    for k in range(days):
        # Make a copy of current image
        oldimg = img.copy()
        # Loop through active pixels
        # Ignore extreme edges
        for row in range(1,rows-1):
            for col in range(1,cols-1):
                # Slice out 3x3 neighborood around current entry
                neighbors = oldimg[(row-1):(row+2), (col-1):(col+2)]
                # Assign next iteration value based on evolve function
                img[row,col]=evolve(neighbors)   
        # Wrap new iteration        
        img = edges(img)
        anim.set_data(img)
        plt.pause(0.01) 
        
        R.append((img==1).sum())
        I.append((img>2).sum())
        V.append((img==2).sum())
        S.append(people - R[-1] - I[-1] - V[-1])
       
        if (img < 3).all():
            break;

fig, ax = plt.subplots(num=3, clear=True)
ax.plot(S, 'go')
ax.plot(I, 'rs')
ax.plot(R, 'm+')
ax.plot(V)   
ax.plot(np.array(S)+np.array(I)+np.array(R)+np.array(V))     
print(k)
