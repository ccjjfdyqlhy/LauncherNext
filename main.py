from ui import main

if __name__ in {"__main__", "__mp_main__"}: # Allow for multiprocessing
    main()
    #import tests.launch