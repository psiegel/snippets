require 'rubygems'
require 'net/smtp'
require 'nokogiri'
require 'open-uri'

DAYS = -1
TEST = false

TO_ADDRESS = 'jenn@binkystick.com'
TO_NAME = 'Jenn'
FROM_ADDRESS = 'root@binkystick.com'
FROM_NAME = 'Pierce'
SUBJECT = 'New UCR Jobs'


def fetch_listings(min_date)
  file = open('https://irecruitportal.ucr.edu/irecruit/!Controller?action=jobs_template&page=jobs_browser&public=true')
  xml_doc = Nokogiri::XML(file)
  nodes = xml_doc.xpath("//*[@category=9]")

  if DAYS > -1
    return nodes.select do |node|
      date_node = node.element_children[6]
      date_str = date_node.text.strip
      listing_date = DateTime.strptime(date_str, '%m/%d/%Y').to_date
      listing_date > min_date
    end
  else
    return nodes
  end
end

def format_html(listings, message)
  template = "<html>
  <head>
    <style>
      table, th, td {
        border: 1px solid black;
      }
    </style>
  </head>
  <body>
    <h3>#{message}</h3>
    <table>
      <thead>
        <tr>
          <th>Job Number</th>
          <th>Working Title</th>
          <th>Category</th>
          <th>Department</th> 
          <th>Location</th>  
          <th>Salary</th> 
          <th>Date Posted</th> 
          <th>Filing Deadline</th>  
        </tr>
      </thead>
      <tbody>
        XXX
      </tbody>
    </table>
  </body>
</html>"
  template.gsub('XXX', listings.map { |l| l.to_s }.join(' '))
end


min_date = DateTime.now.to_date - DAYS
listings = fetch_listings(min_date)
if listings.length > 0
  text = format_html(listings, "Hi Jenn, I found #{listings.count} new listings between #{min_date} and today:")

  message = "From: #{FROM_NAME} <#{FROM_ADDRESS}>
To: #{TO_NAME} <#{TO_ADDRESS}>
MIME-Version: 1.0
Content-type: text/html
Subject: #{SUBJECT}

#{text}"  

  if TEST
    puts message
  else  
    Net::SMTP.start('localhost') do |smtp|
      smtp.send_message(message, FROM_ADDRESS, TO_ADDRESS)
    end
  end
end

