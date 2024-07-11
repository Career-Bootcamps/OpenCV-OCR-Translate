    # data_manager.py save_output_file() 테스트에 사용된 코드
    @classmethod
    def save_output_file(cls, src_file, out_image):
        print ('[DataManager] save_output_file() called...')

        # out_image는 PIL의 Image 객체
        if out_image is None:
            print ('[DataManager] save_output_file() : image is None, it can not be saved!')
       
        # out_file은 path
        out_file = cls.get_output_file()
        print ('[DataManager] save_output_file() : src_file=', src_file)
        print ('[DataManager] save_output_file() : out_file=', out_file)

        # resized for test
        resized_image = out_image.resize((500, 500))        

        if out_file is not None:
            # 확장자에 따라서 저장을 달리함
            cls.__save_according_ext(out_file, resized_image)
            print('[DataManager] save_output_file(): Image saved successfully!')
            return True
        return False