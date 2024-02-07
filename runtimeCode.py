runtimes = []
while True:
    try:
        start_time = time.time()
        get_joystick_pos(button_positions)
        print("--- %s seconds ---" % (time.time() - start_time))
        runtimes.append(time.time() - start_time)
        time.sleep(0.5)
    except:
        KeyboardInterrupt
        break

print(sorted(runtimes))