import multiprocessing
import time
import sys
import NavigationFuture
import UI_GesturCTRL

def run_app():
    with multiprocessing.Manager() as manager:
        shared_data = manager.dict()
        shared_data['mode'] = 0
        shared_data['shutdown'] = False

        p1 = multiprocessing.Process(target=UI_GesturCTRL.run_ui, args=(shared_data,))
        p2 = multiprocessing.Process(target=NavigationFuture.run_navigation, args=(shared_data,))

        p1.start()
        p2.start()

        try:
            while p1.is_alive() and p2.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            shared_data['shutdown'] = True
            p1.terminate()
            p2.terminate()
            p1.join()
            p2.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_app()
