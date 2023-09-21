import csv
import os
import termcolor

class Robot():
    def __init__(self, file_name='example.csv'):
        self.file_name = file_name

        # 名前を聞く
        self.name = self.ask_ques_template(sentence=None, mode='name')

        # ファイルが存在しないなら、新規作成
        if not os.path.exists(file_name):
            try:
                with open(file_name, 'w') as csvfile:
                    csv_writer = csv.writer(csvfile)

                    # ヘッダー行を書きこむ
                    csv_writer.writerow(['NAME', 'COUNT'])

            except Exception as e:
                print('cannot create file : '.format(e))

        # ファイルの中身を保存
        self.data_dict = {}
        with open(self.file_name, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                self.data_dict[row['NAME']] = int(row['COUNT'])
            self.sorted_data = dict(sorted(self.data_dict.items(), key=lambda item: item[1], reverse=True))

    # mode: 'name', 'two', 'what'
    def ask_ques_template(self, sentence, mode):
        frame = termcolor.colored('#' * 30, 'green')
        print(frame)

        if mode == 'two':
            template = f'My favorite restaurant is a {sentence}. Do you like {sentence}?[Yes/No]'
        elif mode == 'what':
            template = f'What is your favorite restaurants, {self.name}?'
        elif mode == 'name':
            template = "Hello! My name is Robot. What is your name?"
        else:
            print('Error Mode')

        colord_sentence = termcolor.colored(template, 'green')
        print(colord_sentence)
        print(frame)

        # 適切な回答を得られるまで繰り返し
        # if mode == 'two':
        #     while True:
        #         answer = input()
        #         answers = answer.split()
        #         capitalized_ans = ''.join(word.capitalize() for word in answers)
        #         if capitalized_ans in ['Yes', 'No']:
        #             break
        answer = input()
        answers = answer.split()
        capitalized_ans = ''.join(word.capitalize() for word in answers)
        return capitalized_ans

    def check_csv(self):
        with open(self.file_name, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                self.data_dict[row['NAME']] = row['COUNT']

            self.sorted_data = dict(sorted(self.data_dict.items(), key=lambda item: item[1], reverse=True))
    def write_csv(self):

        # 既存の店の名前で好きかどうか尋ねる
        for shop_name in self.sorted_data.keys():
            answer = self.ask_ques_template(shop_name, mode='two')
            if answer == 'Yes':
                self.sorted_data[shop_name] += 1
                #self.write_data[shop_name] = self.sorted_data[shop_name]

        # どこのお店が好きか尋ねる
        answer = self.ask_ques_template(sentence=None, mode='what')
        if answer in self.sorted_data.keys():
            self.sorted_data[answer] += 1
            #self.write_data[shop_name] = self.sorted_data[answer]

        else:
            #self.write_data[answer] = 1
            self.sorted_data[answer] = 1

        with open(self.file_name, 'w') as csvfile:
            csv_writer = csv.writer(csvfile)

            # write header
            csv_writer.writerow(['NAME', 'COUNT'])

            #write data
            for name, count in self.sorted_data.items():
                csv_writer.writerow([name, count])


        # csvファイルのデータをチェック
        self.check_csv()
        print(f'{self.name}, thank you!! Have a good day!!')




if __name__ == '__main__':
    robot = Robot()
    #robot.ask_ques_template("what is your name?")
    robot.write_csv()
