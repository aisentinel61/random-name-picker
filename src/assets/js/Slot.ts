interface SlotConfigurations {
  /** User configuration for maximum item inside a reel */
  maxReelItems?: number;
  /** User configuration for whether winner should be removed from name list */
  removeWinner?: boolean;
  /** User configuration for element selector which reel items should append to */
  reelContainerSelector: string;
  /** Number of slots/reels to display */
  numberOfSlots?: number;
  /** User configuration for callback function that runs before spinning reel */
  onSpinStart?: () => void;
  /** User configuration for callback function that runs after spinning reel */
  onSpinEnd?: () => void;

  /** User configuration for callback function that runs after user updates the name list */
  onNameListChanged?: () => void;
}

/** Class for doing random name pick and animation */
export default class Slot {
  /** List of names to draw from */
  private nameList: string[];

  /** Whether there is a previous winner element displayed in reel */
  private havePreviousWinner: boolean[];

  /** Containers that hold the reel items */
  private reelContainers: (HTMLElement | null)[];

  /** Number of slots/reels */
  private numberOfSlots: NonNullable<SlotConfigurations['numberOfSlots']>;

  /** Maximum item inside a reel */
  private maxReelItems: NonNullable<SlotConfigurations['maxReelItems']>;

  /** Whether winner should be removed from name list */
  private shouldRemoveWinner: NonNullable<SlotConfigurations['removeWinner']>;

  /** Reel animation object instances */
  private reelAnimations: (Animation | undefined)[];

  /** Callback function that runs before spinning reel */
  private onSpinStart?: NonNullable<SlotConfigurations['onSpinStart']>;

  /** Callback function that runs after spinning reel */
  private onSpinEnd?: NonNullable<SlotConfigurations['onSpinEnd']>;

  /** Callback function that runs after spinning reel */
  private onNameListChanged?: NonNullable<SlotConfigurations['onNameListChanged']>;

  /**
   * Constructor of Slot
   * @param maxReelItems  Maximum item inside a reel
   * @param removeWinner  Whether winner should be removed from name list
   * @param reelContainerSelector  The base element ID of reel items to be appended
   * @param numberOfSlots  Number of slots/reels to display
   * @param onSpinStart  Callback function that runs before spinning reel
   * @param onNameListChanged  Callback function that runs when user updates the name list
   */
  constructor(
    {
      maxReelItems = 30,
      removeWinner = true,
      reelContainerSelector,
      numberOfSlots = 5,
      onSpinStart,
      onSpinEnd,
      onNameListChanged
    }: SlotConfigurations
  ) {
    this.nameList = [];
    this.numberOfSlots = numberOfSlots;
    this.havePreviousWinner = Array(numberOfSlots).fill(false);
    
    // Initialize multiple reel containers
    this.reelContainers = [];
    for (let i = 1; i <= numberOfSlots; i++) {
      const selector = `${reelContainerSelector}-${i}`;
      this.reelContainers.push(document.querySelector(selector));
    }
    
    this.maxReelItems = maxReelItems;
    this.shouldRemoveWinner = removeWinner;
    this.onSpinStart = onSpinStart;
    this.onSpinEnd = onSpinEnd;
    this.onNameListChanged = onNameListChanged;

    // Create reel animations for each slot
    this.reelAnimations = this.reelContainers.map((reelContainer) => {
      const animation = reelContainer?.animate(
        [
          { transform: 'none', filter: 'blur(0)' },
          { filter: 'blur(1px)', offset: 0.5 },
          { transform: 'translateY(0px)', filter: 'blur(0)' }
        ],
        {
          duration: this.maxReelItems * 100, // 100ms for 1 item
          easing: 'ease-in-out',
          iterations: 1
        }
      );
      animation?.cancel();
      return animation;
    });
  }

  /**
   * Setter for name list
   * @param names  List of names to draw a winner from
   */
  set names(names: string[]) {
    this.nameList = names;

    // Clear all reel containers
    this.reelContainers.forEach((reelContainer, index) => {
      const reelItemsToRemove = reelContainer?.children
        ? Array.from(reelContainer.children)
        : [];

      reelItemsToRemove.forEach((element) => element.remove());
      this.havePreviousWinner[index] = false;
    });

    if (this.onNameListChanged) {
      this.onNameListChanged();
    }
  }

  /** Getter for name list */
  get names(): string[] {
    return this.nameList;
  }

  /**
   * Setter for shouldRemoveWinner
   * @param removeWinner  Whether the winner should be removed from name list
   */
  set shouldRemoveWinnerFromNameList(removeWinner: boolean) {
    this.shouldRemoveWinner = removeWinner;
  }

  /** Getter for shouldRemoveWinner */
  get shouldRemoveWinnerFromNameList(): boolean {
    return this.shouldRemoveWinner;
  }

  /**
   * Returns a new array where the items are shuffled
   * @template T  Type of items inside the array to be shuffled
   * @param array  The array to be shuffled
   * @returns The shuffled array
   */
  private static shuffleNames<T = unknown>(array: T[]): T[] {
    const keys = Object.keys(array) as unknown[] as number[];
    const result: T[] = [];
    for (let k = 0, n = keys.length; k < array.length && n > 0; k += 1) {
      // eslint-disable-next-line no-bitwise
      const i = Math.random() * n | 0;
      const key = keys[i];
      result.push(array[key]);
      n -= 1;
      const tmp = keys[n];
      keys[n] = key;
      keys[i] = tmp;
    }
    return result;
  }

  /**
   * Function for spinning the slot
   * @returns Whether the spin is completed successfully
   */
  public async spin(): Promise<boolean> {
    if (this.nameList.length < this.numberOfSlots) {
      console.error(`Name List must have at least ${this.numberOfSlots} names. Cannot start spinning.`);
      return false;
    }

    if (this.onSpinStart) {
      this.onSpinStart();
    }

    const { shouldRemoveWinner } = this;
    
    // Select unique winners for each slot
    const shuffledNames = Slot.shuffleNames<string>(this.nameList);
    const winners: string[] = shuffledNames.slice(0, this.numberOfSlots);

    // Animate each reel
    const animationPromises: Promise<void>[] = [];

    for (let slotIndex = 0; slotIndex < this.numberOfSlots; slotIndex++) {
      const reelContainer = this.reelContainers[slotIndex];
      const reelAnimation = this.reelAnimations[slotIndex];

      if (!reelContainer || !reelAnimation) {
        continue;
      }

      // Create shuffled names for this reel
      let randomNames = Slot.shuffleNames<string>(this.nameList);
      
      while (randomNames.length && randomNames.length < this.maxReelItems) {
        randomNames = [...randomNames, ...randomNames];
      }

      randomNames = randomNames.slice(0, this.maxReelItems - Number(this.havePreviousWinner[slotIndex]));
      
      // Replace the last item with the designated winner for this slot
      randomNames[randomNames.length - 1] = winners[slotIndex];

      const fragment = document.createDocumentFragment();

      randomNames.forEach((name) => {
        const newReelItem = document.createElement('div');
        newReelItem.innerHTML = name;
        fragment.appendChild(newReelItem);
      });

      reelContainer.appendChild(fragment);

      console.info(`Slot ${slotIndex + 1} - Winner: ${winners[slotIndex]}`);

      // Calculate the actual height of the reel after rendering
      const reelHeight = reelContainer.scrollHeight;
      const firstItemHeight = reelContainer.children[0]?.getBoundingClientRect().height || 120;
      const translateDistance = reelHeight - firstItemHeight;

      // Update animation with actual calculated distance
      reelAnimation.effect = new KeyframeEffect(
        reelContainer,
        [
          { transform: 'none', filter: 'blur(0)' },
          { filter: 'blur(1px)', offset: 0.5 },
          { transform: `translateY(-${translateDistance}px)`, filter: 'blur(0)' }
        ],
        {
          duration: this.maxReelItems * 100,
          easing: 'ease-in-out',
          iterations: 1
        }
      );

      // Play the spin animation
      const animationPromise = new Promise<void>((resolve) => {
        reelAnimation.onfinish = () => resolve();
      });

      reelAnimation.play();
      animationPromises.push(animationPromise);
    }

    // Remove winners from name list if necessary
    if (shouldRemoveWinner) {
      winners.forEach((winner) => {
        const index = this.nameList.findIndex((name) => name === winner);
        if (index !== -1) {
          this.nameList.splice(index, 1);
        }
      });
    }

    console.info('All Winners: ', winners);
    console.info('Remaining: ', this.nameList);

    // Wait for all animations to complete
    await Promise.all(animationPromises);

    // Clean up and finish animations
    this.reelContainers.forEach((reelContainer, index) => {
      const reelAnimation = this.reelAnimations[index];
      
      if (reelContainer && reelAnimation) {
        // Sets the current playback time to the end of the animation
        reelAnimation.finish();

        // Remove all items except the last one (the winner)
        Array.from(reelContainer.children)
          .slice(0, reelContainer.children.length - 1)
          .forEach((element) => element.remove());

        this.havePreviousWinner[index] = true;
      }
    });

    if (this.onSpinEnd) {
      this.onSpinEnd();
    }
    
    return true;
  }
}
