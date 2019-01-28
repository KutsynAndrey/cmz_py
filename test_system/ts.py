import subprocess
import os
import time
import resource


copy_path = os.getcwd()


def get_input(problem_name, number):
    test_file = open(os.getcwd() + '/tests/input/' + problem_name + '/' + str(number) + '.txt')
    return test_file


def get_output(problem_name, number):
    test_file = open(os.getcwd() + '/tests/output/' + problem_name + '/' + str(number) + '.txt')
    return test_file


def test(solution, problem_name):
    verdict = set()
    result = []
    compilation_time = ''
    mid_compilation_time = 0
    os.chdir(os.getcwd() + '/test_system')

    problem = open('main.cpp', 'w')
    problem.write(solution)
    problem.close()

    answer = ''
    ram = ''
    p = subprocess.Popen(["g++", "main.cpp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if err.decode() == '':
        for i in range(1, len(os.listdir('tests/input/' + problem_name))+1):
            test_input = get_input(problem_name, i)
            test_input = test_input.read()
            test_output = get_output(problem_name, i)
            test_output = test_output.read()

            process = subprocess.Popen("./a.out", stdout=subprocess.PIPE, stdin=subprocess.PIPE)
            start_time = time.time()
            data = process.communicate(input=(str.encode(str(test_input))))
            process.wait()
            memory = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss // 1024
            result_time = time.time() - start_time
            ram += "%s\n" % str(memory)
            mid_compilation_time += float(result_time)
            print(result_time, '\n')
            compilation_time += '%s\n' % str(result_time)
            print(data[0].decode(), '\n', test_output, '\n')
            if data[0].decode() == '':
                answer += "PE\n"
                verdict.add('PE')
            elif data[0].decode() == test_output:
                answer += "OK\n"
                verdict.add('OK')
            else:
                answer += "WA\n"
                verdict.add('WA')
        result.append(answer)
        result.append(create_str_verdict(verdict))
        result.append(compilation_time)
        result.append(ram)
        result.append(mid_compilation_time / len(os.listdir('tests/input/' + problem_name)))
        os.chdir(copy_path)
        ans = (result, "not found")
        return ans

    else:
        for i in range(1, len(os.listdir('tests/input/' + problem_name))+1):
            answer += "CE\n"
            compilation_time += '0.00000\n'
            ram += '0\n'
        mid_compilation_time = '0.00000'
        result.append(answer)
        result.append("CE")
        result.append(compilation_time)
        result.append(ram)
        result.append(mid_compilation_time)
        ans = (result, err.decode())
        return ans


def create_str_verdict(verdict_set):
    result = ''
    if len(verdict_set) == 1:
        for param in verdict_set:
            result += param
        return result
    for param in verdict_set:
        if param != 'OK':
            result += param
            result += ' '

    return result











