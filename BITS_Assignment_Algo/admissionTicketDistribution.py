from pathlib import Path

output_file_name = "SampleOutputPS08.txt"
input_file_name = "SampleInputPS08.txt"


class AdmissionTicketDistribution(object):

    # c : number of counter
    # n : number of student
    def __init__(self, c, n):
        self.c = c
        self.n = n
        self.queues = [[None for i in range(n)] for j in range(c)]
        self.starts = [0 for i in range(c)]
        self.ends = [0 for i in range(c)]
        self.sizes = [0 for i in range(c)]
        self.open = [False for i in range(c)]
        self.open[0] = True

    # return the counter status
    def is_counter_open(self, counter_id):
        return self.open[counter_id - 1]

    # add the student in queue
    def enqueue(self, student_id, counter_id):
        queue_index = self.queues[counter_id - 1].index(None)
        self.queues[counter_id - 1][queue_index] = student_id

    # validate queue is empty
    def is_queue_empty(self, counter_id):
        if not self.is_counter_open(counter_id):
            return True
        if None in self.queues[counter_id - 1] and \
                self.queues[counter_id - 1].index(None) == 0:
            return True
        else:
            return False

    # Remove the student from queue
    def dequeue(self, counter_id):
        if self.is_queue_empty(counter_id):
            return -1
        else:
            student = self.queues[counter_id - 1][0]
            del self.queues[counter_id - 1][0]
            self.queues[counter_id - 1].append(None)
            return student

    # counter_id : pass the counter id
    # return the list of open counter
    def get_counter_number(self, counter_id):
        counter = []
        for counter_item in self.queues[counter_id - 1]:
            if counter_item is not None:
                counter.append(counter_item)
        return counter

    # return the queue size
    def queue_size(self, counter_id):
        if None not in self.queues[counter_id - 1]:
            return self.n
        else:
            return self.queues[counter_id - 1].index(None)

    # Insert student into queue
    def insert_student_into_queue(self):
        get_open_counter = self.open.index(False)
        minimum_queue = self.queue_size(1)
        counter = 1
        for i in range(1, get_open_counter + 1):
            length_of_queue = self.queue_size(i)
            if minimum_queue > length_of_queue:
                minimum_queue = length_of_queue
                counter = i
        if minimum_queue == self.n:
            if get_open_counter == self.c:
                return -1
            else:
                self.open[get_open_counter] = True
                counter = get_open_counter
                return counter + 1
        else:
            return counter

    # add the student in row
    def add_student(self, student_id):
        counter = self.insert_student_into_queue()
        if counter == -1:
            return "Counter is full, That student need not be considered in " \
                   "the next iteration"
        else:
            self.enqueue(student_id, counter)
            return counter

    # give admission ticket to student
    def give_admission_ticket(self):
        ticket = 0
        for i in range(self.c):
            queue_result = self.dequeue(i)
            if queue_result != -1:
                ticket += 1
        if ticket == 0:
            return "Queue is Empty !!"
        else:
            return ticket


# split the input file
def split_input_file_data(file):
    input_data = file.strip().split(':')
    if len(input_data) == 3:
        return int(input_data[1]), int(input_data[2])
    elif len(input_data) == 2 and input_data[-1]:
        return int(input_data[-1])
    else:
        return 'Invalid Input !!!'


if __name__ == "__main__":
    open(output_file_name, 'w').close()
    output_file = open(output_file_name, "a")
    input_file = Path(__file__).with_name(input_file_name)
    with open(input_file) as file:
        for line in file:
            input_value = split_input_file_data(line)
            output = None
            formatted_output = None
            if line.startswith('ticketSystem'):
                admissionTicketDistribution = \
                    AdmissionTicketDistribution(input_value[0], input_value[1])
            elif line.startswith('addStudent'):
                output = admissionTicketDistribution.add_student(input_value)
                formatted_output = line.strip() + " >> " + str(output)
            elif line.startswith('getCounter'):
                output = admissionTicketDistribution.get_counter_number(input_value)
                formatted_output = line.strip() + " >> " + str(output)
            elif line.startswith('isOpen'):
                output = admissionTicketDistribution.is_counter_open(input_value)
                formatted_output = line.strip() + " >> " + str(output)
            elif line.startswith('giveAdmissionTicket'):
                output = admissionTicketDistribution.give_admission_ticket()
                formatted_output = line.strip() + " >> " + str(output)
            else:
                print('Wrong Input!!!')

            #write the output into file
            if str(output) != 'None':
                output_file.write(formatted_output + '\n')

        file.close()
        output_file.close()
        print("Output file " + " '" + output_file_name + "'  created")
